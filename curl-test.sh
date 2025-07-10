#!/bin/bash

# Function to generate a random alphanumeric string of variable length (up to 15 characters)
random_string() {
  alphabetNumeric="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
  alphabetNumericLength=${#alphabetNumeric}
  for i in $(seq 1 $(( $RANDOM % 16 ))); do
    randomIndex=$(( RANDOM % alphabetNumericLength ))
    randomString+="${alphabetNumeric:$randomIndex:1}"
  done

  echo $randomString
}

# Generate random data for the new timeline post
name=$(random_string)
email=$(random_string)@test.com
content=$(random_string)

# Send a POST request to create a new timeline post and capture the returned ID
newID=$(
  curl -X POST \
  http://localhost:5000/api/timeline_post \
  -d "name=$name&email=$email&content=$content" \
   | jq -r '.id'
)

# Fetch the newly created timeline post using the returned ID
data=$(curl "http://localhost:5000/api/timeline_post?id=$newID")


# Validate that the returned data matches the data sent in the POST request
if [ $name != $(echo $data | jq -r '.name') ]; then
  echo "Name mismatch: expected $name, got $(echo $data | jq -r '.name')"
  exit 1
fi
if [ $email != $(echo $data | jq -r '.email') ]; then
  echo "Email mismatch: expected $email, got $(echo $data | jq -r '.email')"
  exit 1
fi
if [ $content != $(echo $data | jq -r '.content') ]; then
  echo "Content mismatch: expected $content, got $(echo $data | jq -r '.content')"
  exit 1
fi
echo "Test passed: POST and GET requests are successful."
