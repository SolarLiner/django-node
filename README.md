# `django_node`

An experiment in making Node.js SSR available to Django.

# Context

Django provides an excellent and mature ORM system simplifying descriptions of 
structured data. On the front-end side, JavaScript has a mature web application
library, making it easy through the use of frameworks and libraries to create rich
web applications.  
However, at first the HTML was generated through DOM manipulation directly in the
browser, making low-end devices struggle to display those applications.

One of the many solutions to this problem is to render a version of the HTML on the
server before having the client "hydrate" the HTML - that is to say reconciliate the
server HTML with its internal representation, which is faster than starting on the
client from scratch. However, these techniques require JavaScript to be run on the
server, essentially rendering this technique innaccessible from any other platform
than Node.js itself.

The use-case behind this approach is to be able to use Django's ORM while being
able to use SSR to boost performance on web browsers.

# The approach

A first version of this used a naive "transitive node process" approach where the 
node executable was launched with the frontend script for every request. This worked
and helped iron out the API surface but proved to be too resource-intensive and slow
for even the lightest of workloads.

This version uses [ZeroMQ](https://zeromq.org/) to transfer a JSON string out of the
Django server process into the node process, and take a string in from the Node 
process (i.e. containing the resulting HTML) and back to the Django server. In the
current approach, the Node process is in charge of outputing *all* the HTML; basically
the Django server process acts as a proxy for the Node server.

Because the messaging system is implemented with ZeroMQ, there is no additional
overhead of bringing up an additional HTTP server on the Node process; and ZeroMQ has
proven itself to be reliable.

## The Django infrastrcture

Most of the work is pulled by an implementation of `HttpResponse` that sends a
Python dictionary encoded as JSON and passed through ZeroMQ as a string in request
mode. [`NodeHttpResponse`](noderesponse/http.py) then waits for a response that it will take to be the body
of the response for the Django server.  

The communication is triggered on the first access to the `NodeHttpResponse.connect`
property. This property access is idempotent - the communication will only be triggered
once for the instance, and the response is cached and re-used on any subsequent
`connect` access.

The [`NodeResponseMixin`](noderesponse/views.py) mixin is a sibling of 
`SimpleTemplateResponse` in spirit - it, along with `NodeView`, the counterpart of `View`
allows all of the higher-level features of Django views to work seamlessly to the
user. Most of the classes in [the `generic` module](noderesponse/generic) are direct
re-implementation (even reusing Django code by assigning functions directly in the 
new classes) of the generic Django view, allowing for simple creation of Node.js-based
views. As an example, see [`views.py`](example_nodeview/views.py) in the example Django
application.

## The Node.js infrastructure

The Node process sets up a ZeroMQ server which listens for incoming messages. Its job
is to deserialize the JSON string and process the request (typically this should be
implemented in its own module to hide the implementation details, and leaving the 
request processing to end-users), before sending back the generated HTML (hardcoded
content-type for now, the response could be changed to allow the Node.js server to
set the content-type itself) to the Django process.

In fact, there is nothing locking the setup to Node.js only, any process which setups
a ZeroMQ server can be used here; the process isn't managed by Django and must be
started manually.

# Conclusion

While brittle and definitely not production-ready, this approach has the advantage of
allowing Node.js-backed SSR to feature in monolithic server deployment scenarios, and
in a lighter fashion than having two HTTP servers running on one machine, proxying
requests back and forth.
