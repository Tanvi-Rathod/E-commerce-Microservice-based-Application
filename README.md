1. Requirements
• Programming Language: Python (for each microservice backend)
• Databases:
o MongoDB Atlas: NoSQL database for storing service data.
o Redis: In-memory data structure store, used for caching and Pub/Sub 
messaging.
• Microservices Framework: Flask (Python web framework)
• API Gateway: NGINX (for centralized request routing)
• Monitoring: Prometheus (metrics collection) and Grafana (metrics visualization)
• Containerization: Docker and Docker Compose for deployment and dependency 
management

2. Architecture Overview
Because each service represents an independent module, it takes care of one particular 
function within the e-commerce domain. Their interactions are only through HTTP requests, 
thus giving them a low coupling. Moreover, a shared Docker network allows for seamless 
communications between the services while logically isolating them from external 
environments. 
Core Services:
• Product Service: Manages product catalog, supports CRUD operations.
• Cart Service: Handles shopping cart data for users.
• User Service: Manages user profiles and authentication.
• Order Service: Processes orders and maintains order history.
Supporting Components:
• API Gateway (NGINX): Routes incoming requests to respective services.
• MongoDB Atlas: Stores service-specific data in individual collections.
• Redis: Provides caching for quicker data access and Pub/Sub channels for real-time 
notifications.
• Prometheus and Grafana: Collects and visualizes performance and usage metrics.
3. Service Details
Product Service
• Purpose: Manages product data including details like name, price, and description.
• Endpoints:
o POST /product: Create a new product.
o GET /product/<id>: Retrieve product details by ID.
o PUT /product/<id>: Update product information.
o DELETE /product/<id>: Delete a product.
• Database: MongoDB stores product data.
Cart Service
• Purpose: Manages users' shopping cart data.
• Endpoints:
o POST /cart: Add items to a user’s cart.
o GET /cart/<user_id>: Retrieve cart items for a user.
o DELETE /cart/<user_id>: Clear a user’s cart.
• Database: MongoDB stores cart data, with caching handled by Redis.
User Service
• Purpose: Manages user profile information.
• Endpoints:
o POST /user: Register a new user.
o GET /user/<id>: Get user details.
o PUT /user/<id>: Update user profile.
o DELETE /user/<id>: Delete user profile.
• Pub/Sub: Publishes user creation and deletion events to Redis.
Order Service
• Purpose: Handles order processing.
• Endpoints:
o POST /order: Place a new order.
o GET /order/<user_id>: Retrieve orders for a user.
o DELETE /order/<order_id>: Cancel an order.
• Database: Stores order data in MongoDB.
4. Dependencies and Installation
To run the application, ensure the following dependencies are installed and configured:
• Docker and Docker Compose:
o Install Docker and Docker Compose to containerize services.
bash
sudo apt-get update
sudo apt-get install -y docker.io docker-compose
• MongoDB Atlas:
o Create an account on MongoDB Atlas, set up a cluster, and whitelist IPs as 
needed.
o Define the MONGO_URI environment variable to use the MongoDB 
connection string.
• Redis:
o Redis is hosted as a containerized service in Docker Compose. Redis 
Pub/Sub is enabled by default.
• Prometheus and Grafana:
o Prometheus and Grafana containers are configured via Docker Compose.
o Ensure ports 9090 (Prometheus) and 3000 (Grafana) are open on your local 
environment.
5. Execution Flow
1. API Gateway receives an HTTP request and forwards it to the relevant service.
2. Microservice performs the requested action, interacting with MongoDB for persistent 
data storage and Redis for caching or Pub/Sub messages when required.
3. Response is sent back through the API Gateway to 
