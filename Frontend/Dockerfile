# Use the official Nginx image from Docker Hub
FROM nginx:alpine

# Copy your custom Nginx configuration file
COPY nginx.conf /etc/nginx/nginx.conf

# Copy the entire frontend directory content into Nginx's web root
COPY . /usr/share/nginx/html

# Expose port 80 to access the frontend application
EXPOSE 80
