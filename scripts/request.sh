curl --location --request POST 'http://127.0.0.1:3000/people/count' \
--header 'Content-Type: application/json' \
--data '{
    "image": "data/dogcatperson.jpeg",
    "type": "path"
}'
