const AWS = require("aws-sdk");
const dynamodb = new AWS.DynamoDB({ apiVersion: "2012-08-10" });

exports.handler = async event => {
  console.log("Input to the lambda function", event);
  let { shortURL } = event;
  shortURL = shortURL.split('https://test.com/')[1]
  return dynamodb
    .getItem({
      TableName: "URL-Shortener",
      Key: {
        shortid: { S: shortURL }
      }
    })
    .promise()
    .then(response => {
      console.log("response from DDB", response);
      return {
        statusCode: 302,
        headers: {
          Location: response.Item.long_url.S
        }
      };
    })
    .catch(err => {
      console.error("error while fetching data from DDB", err);
      return err;
    });
};
