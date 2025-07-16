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
echo "Generated data: Name=$name, Email=$email, Content=$content"

# try Send a POST request to create a new timeline post and capture the returned ID
newID=$(
  curl -X POST \
  http://localhost:5000/api/timeline_post \
  -d "name=$name&email=$email&content=$content" \
   | jq -r '.id'
)
# Check if the newID is empty, indicating that the POST request failed
if [ -z "$newID" ]; then
  echo "Failed to create a new timeline post."
  exit 1
else
  echo "New timeline post created with ID: $newID"
fi

# Fetch the newly created timeline post using the returned ID
data=$(curl "http://localhost:5000/api/timeline_post")
# check all posts to find the one with the new ID and if not found, exit with an error
if ! echo "$data" | jq -e '.timeline_posts[] | select(.id == '"$newID"')' > /dev/null; then
  echo "New timeline post with ID $newID not found."
  exit 1
else
  echo "New timeline post with ID $newID found."
fi


# if post exists, fetch the specific post using the new ID
data=$(curl "http://localhost:5000/api/timeline_post/$newID")
# if the data is empty, it indicates that the GET request failed
if [ -z "$data" ]; then
  echo "Failed to fetch the timeline post with ID $newID."
  exit 1
else
  echo "Fetched timeline post with ID $newID successfully."
fi

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
# If all validations pass, print success message
echo "Data validation successful: Name, Email, and Content match the POST request."


# Array of test cases with missing fields
declare -A test_cases=(
  ["name"]="Invalid Name"
  ["email"]="Invalid Email"
  ["content"]="Invalid Content"
)

# Loop through each test case
for field in "${!test_cases[@]}"; do
  # Prepare data with the current field missing
  case $field in
    "name")
      test_name=""
      test_email=$email
      test_content=$content
      ;;
    "email")
      test_name=$name
      test_email=""
      test_content=$content
      ;;
    "content")
      test_name=$name
      test_email=$email
      test_content=""
      ;;
  esac

  # Send the POST request
  response=$(curl -s -X POST \
    http://localhost:5000/api/timeline_post \
    -d "name=$test_name&email=$test_email&content=$test_content")

  # Extract the error message from the response
  error_message=$(echo "$response" | jq -r '.error' | xargs)

  # Check if the error message matches the expected error
  expected="${test_cases[$field]}"
  if [ "$error_message" != "$expected" ]; then
    echo "Test failed for missing $field: expected error '$expected', got '$error_message'"
    exit 1
  fi


  echo "Test passed for missing $field: received expected error '${test_cases[$field]}'"
done

echo "Test passed: POST and GET requests are successful."
