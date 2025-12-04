FROM nginx:latest

# Install python & pip
RUN apt update && apt install -y python3-flask

# Create custom user 'brandon'
RUN useradd -m brandon

# Copy all project into container
COPY ./app /app
WORKDIR /app

# Replace nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Run Flask on port 5000 and start nginx
CMD python3 app.py & nginx -g "daemon off;"
