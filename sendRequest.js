const axios = require('axios');
const fs = require('fs'); // Import the file system module

async function sendRequest() {
    const url = 'http://localhost:5000/path';
    const data = {
        obstacles: [
            { x: 5, y: 5, d: 0, id: 1 },
            { x: 8, y: 8, d: 2, id: 5 },
            { x: 10, y: 12, d: 4, id: 7 },
            { x: 17, y: 1, d: 6, id: 2 }
        ],
        robot_x: 1,
        robot_y: 1,
        robot_dir: 0,
        retrying: false
    };

    try {
        const response = await axios.post(url, data, {
            headers: {
                'Content-Type': 'application/json' // optional, but recommended
            }
        });
        
        // Log the response to the console
        console.log('Response:', response.data);
        
        // Create a file and write the response data to it
        fs.writeFileSync('sample_response.json', JSON.stringify(response.data, null, 2), 'utf8');
        console.log('Response data has been written to response.json');
        
    } catch (error) {
        console.error('Error:', error.message);
    }
}

sendRequest();
