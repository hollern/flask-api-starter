# Flask API Starter
A simple starting project for any REST API. This project was designed with a particular end use in mind and is designed to support a React front-end. But, can be used for any web app that utilizes AJAX. It has the following features:
- security with JSON Web Tokens (JWT)
- data validation with marshmallow
- dynamic generation of SQLAlchemy queries using custom QueryBuilder module
- supports a multi-tenant SaaS approach
- forgot password, change password functionality

## Organization
This project is organized into the following packages:
- models
- routes
- services
- templates
- views

### Models
This package contains a module for each of the models that are used by the application. In addition to the model a schema exists within each module that allows for defined fields to be verified when loading and dumping inbound and outbound data. Both the models and schemas inherit from a "Core" class. These classes are found in app.models.utils. The core classes (CoreModel and CoreSchema) contain common attributes for each of the respective classes. Additionally app.models.utils also contains exceptions that are common to the models.

### Routes
This package contains a route for each of the resources to be modeled within the REST construct, and should match the models package very closely. In most of the modules, the endpoints are limited to common CRUD logic and utilize functions in app.routes.utils.methods to perform the necessary actions for each CRUD action. In this application, CRUD follows POST, GET, PATCH, and DELETE. Note, PUT is not utilized in this application. There are several other modules within the app.routes.utils package.

QueryBuilder (within query_builder) is a custom class that allows dynamic generation of SQLAlchemy queries based on GET endpoint url arguments. Marshmallow is also used to validate the incoming GET request arguments. QueryBuilder supports filtering, sorting, and pagination. Filtering supports the following comparison operators:
- equals
- less than
- greater than
- less than equals
- greater than equals
- not equals
- in (list)
- like

More details about the QueryBuilder class and formatting the GET request arguments can be found in this same module within the RequestDataSchema class.

Another module, security, is utilized to verify the identity of the requester. For example, there is a function to get the current user based on the JWT. Additionally, the security module is used to set and check the database tenant.

### Services
This package is primarily focused on connecting with external web services, such as Twilio and SendGrid. Currently, this is solely used for connecting with SendGrid to provide support for transactional email.

### Templates
This directory contains HTML templates. Currently, it only contains emails templates.

### Views
This package should contain only one route, the entry-point to the React front-end.