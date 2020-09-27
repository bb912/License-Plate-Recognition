# License-Plate-Recognition
ShellHacks2020: Auto Nation challenge. Camera to Model to Twilio bot for License Plate detection.

-- For specifications on running the models and for more datasets: http://www.inf.ufrgs.br/~crjung/alpr-datasets/

-- Flask frontend with camera uses either motion detection or deterministic script to capture frames from the video feed, and send them via bytestream over the cloud to a separate google cloud computing instance handling the computer vision model for license plate recognition.

-- The Model send an object with the contained License plate No.'s back, and flask then interfaces with the database to lookup the customer of the license plate.

-- We use a mock SQLite3 database to hold information in two related tables, one with customers and one with service appointments.

-- We use Twilio API to text users and/or Service Assistants to notify about arrivals.

--Leverage serverless google cloud infrastructure
