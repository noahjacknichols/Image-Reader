var express = require('express');
var router = express.Router();
const vision = require('@google-cloud/vision');
var fs = require('fs');
var readableStream = fs.createReadStream('../images/preface.jpg');
var data = '';




async function quickstart() {
    //Imports the Google Cloud client library
    const client = new vision.ImageAnnotatorClient();
    fileName = '';
    // Performs text detection on the local file
    const [result] = await client.textDetection(`gs://declr-bucket/preface.jpg`);
    const detections = result.textAnnotations;
    console.log('Text:');
    // detections.forEach(text => console.log(text));
    console.log(detections[0].description);

    return detections[0].description
  }

router.get('/', async (req, res) => {
    console.log("getColumns:");
    console.log(req.query)

    let response = await quickstart();
    response = response.replace(/(\r\n|\n|\r)/gm," ");
    console.log("RESPONSE:")
    console.log(response)

    res.json(response);


});

module.exports = router;
