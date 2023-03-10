const express = require('express')
const {spawn} = require('child_process');
const app = express()
const port = 3000

awsKey = `AKIAIOSFODNN7EXAMPLE`
secret = `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`

app.post('/', (req, res) => {
    try {
        const { url } = req.body
        var dataToSend;
        // spawn new child process to call the python script
        const python = spawn('python', ['script1.py', url]);
        // collect data from script
        python.stdout.on('data', function (data) {
        console.log('Pipe data from python script ...');
        dataToSend = data.toString();
        });
        // in close event we are sure that stream from child process is closed
        python.on('close', (code) => {
        console.log(`child process close all stdio with code ${code}`);
        // send data to browser
        res.send(dataToSend)
        });

    } catch (err) {
        console.log(err.toString());
        res.status(200).send('Failed')
    }
})

app.listen(port, () => console.log(`Example app listening on port ${port}!`))
