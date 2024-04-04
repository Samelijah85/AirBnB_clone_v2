#!/usr/bin/env bash
#  A Bash script that sets up web servers for the deployment of web_static
if dpkg -l | grep -qw nginx; then
    echo "Nginx is installed."
else
    # Update package lists and install Nginx quietly
    sudo apt-get update -qq > /dev/null 2>&1
    sudo apt-get install -y nginx -qq > /dev/null 2>&1

    # Start Nginx and enable it to run on boot, silently
    sudo service nginx start > /dev/null 2>&1
    sudo systemctl enable nginx > /dev/null 2>&1
    # Echo command to confirm completion
    echo "Nginx installation is complete."
fi
# Create a directory if it doesn't exist

# Variables for directory paths
directory_name="/data/"
sud_web_static="/data/web_static/"
sud_releases="/data/web_static/releases/"
sud_shared="/data/web_static/shared/"
sud_test="/data/web_static/releases/test/"
fake_file="/data/web_static/releases/test/index.html"

# Function to create directory if it doesn't exist
create_directory() {
    if [ ! -d "$1" ]; then
        mkdir -p "$1"
        echo "Directory created: $1"
    else
        echo "Directory already exists: $1"
    fi
}

# Create directories
create_directory "$directory_name"
create_directory "$sud_web_static"
create_directory "$sud_releases"
create_directory "$sud_shared"
create_directory "$sud_test"

# Create a fake index.html file
if [ ! -f "$fake_file" ]; then
    echo "Hello world" > "$fake_file"
    echo "File created: $fake_file"
else
    echo "File already exists: $fake_file"
fi

# Create or recreate a symbolic link to the test folder

# Variables for directory paths
link_name="/data/web_static/current"
target_folder="/data/web_static/releases/test/"

# Check if the symbolic link already exists
if [ -L "$link_name" ]; then
    # Remove the existing symbolic link
    rm "$link_name"
fi

# Create a new symbolic link
ln -s "$target_folder" "$link_name"
echo "Symbolic link created: $link_name -> $target_folder"
# Target directory
directory="/data/"

# Change ownership to ubuntu user and group, recursively
sudo chown -R ubuntu:ubuntu "$directory"

echo "Ownership of $directory and its contents has been changed to the ubuntu user and group."

# Update the Nginx configurations
# Define variables
NGINX_CONF='/etc/nginx/sites-available/default'
BACKUP_CONF="${NGINX_CONF}.backup.$(date +%F-%H-%M-%S)"
HBNB_STATIC_CONFIG='\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}'

# Step 1: Backup the original Nginx configuration
echo "Backing up the original Nginx configuration..."
cp "$NGINX_CONF" "$BACKUP_CONF"

# Step 2: Update Nginx configuration
echo "Updating Nginx configuration to serve /data/web_static/current/ under /hbnb_static..."

# Check if the configuration already exists
if grep -q "location /hbnb_static" "$NGINX_CONF"; then
    echo "HBNB_static configuration already exists. Skipping insertion."
else
    # Using awk to insert the configuration before the last "}" to ensure it's inside the server block
    awk "/^}/ {print \"$HBNB_STATIC_CONFIG\"} {print}" $NGINX_CONF > temp && mv temp $NGINX_CONF
fi

# Step 3: Test Nginx configuration
echo "Testing Nginx configuration..."
nginx -t >/dev/null 2>&1

# shellcheck disable=SC2181
if [ "$?" -ne 0 ]; then
    echo "Nginx configuration test failed. Reverting changes..."
    cp "$BACKUP_CONF" "$NGINX_CONF"
    nginx -t && echo "Reverted to the original configuration successfully."
    exit 1
else
    echo "Nginx configuration test passed."
fi

# Step 4: Restart Nginx to apply changes
echo "Restarting Nginx to apply changes..."
sudo service nginx restart

# shellcheck disable=SC2181
if [ $? -eq 0 ]; then
    echo "Nginx restarted successfully. Your content should now be available at /hbnb_static."
else
    echo "Failed to restart Nginx. Please check the system's service status."
fi