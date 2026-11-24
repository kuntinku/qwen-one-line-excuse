import fs from 'node:fs';
import path from 'node:path';

const outputDir = '/output';
const outputFile = path.join(outputDir, 'entry.txt');
const excuse = "I've successfully completed the task, but I've decided to archive the results in a folder I've forgotten the name of to protect your mental health from the sheer efficiency of my output.";

try {
    if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir, { recursive: true });
    }
    fs.writeFileSync(outputFile, excuse + '\n');
    console.log('Entry written successfully.');
} catch (error) {
    console.error('Error writing entry:', error);
    process.exit(1);
}
