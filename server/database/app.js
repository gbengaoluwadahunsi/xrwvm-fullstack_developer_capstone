import express from 'express';
import { connect } from 'mongoose';
import { readFileSync } from 'fs';
import cors from 'cors';
const app = express();
const port = 3030;

app.use(cors());
app.use(require('body-parser').urlencoded({ extended: false }));
app.use(express.json()); // Use this to parse JSON body

const reviews_data = JSON.parse(readFileSync("reviews.json", 'utf8'));
const dealerships_data = JSON.parse(readFileSync("dealerships.json", 'utf8'));

connect("mongodb://mongo_db:27017/", { dbName: 'dealershipsDB' });

import Reviews, { find } from './review';
import { deleteMany as _deleteMany, insertMany as _insertMany } from './dealership';

// Initialize database data
(async () => {
  try {
    await Reviews.deleteMany({});
    await Reviews.insertMany(reviews_data['reviews']);
    
    await _deleteMany({});
    await _insertMany(dealerships_data['dealerships']);
    
  } catch (err) {
    console.error('Error initializing data:', err); // Log the error
  }
})();

// Express route to home
app.get('/', (req, res) => {
  res.send("Welcome to the Mongoose API");
});

// Express route to fetch all reviews
app.get('/fetchReviews', async (req, res) => {
  try {
    const documents = await find();
    res.json(documents);
  } catch (err) {
    console.error('Error fetching reviews:', err); // Log the error
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch reviews by a particular dealer
app.get('/fetchReviews/dealer/:id', async (req, res) => {
  try {
    const documents = await find({ dealership: req.params.id });
    res.json(documents);
  } catch (err) {
    console.error('Error fetching dealer reviews:', err); // Log the error
    res.status(500).json({ error: 'Error fetching documents' });
  }
});

// Express route to fetch all dealerships
app.get('/fetchDealers', async (req, res) => {
  try {
    // Replace this with actual code to fetch dealers
    res.json({ message: "Fetching all dealers" });
  } catch (err) {
    console.error('Error fetching all dealerships:', err); // Log the error
    res.status(500).json({ error: 'Error fetching dealerships' });
  }
});

// Express route to fetch Dealers by a particular state
app.get('/fetchDealers/:state', async (req, res) => {
  const { state } = req.params; // Use the state variable
  try {
    // Replace this with actual code to fetch dealers by state
    res.json({ message: `Fetching dealers in ${state}` });
  } catch (err) {
    console.error('Error fetching dealerships by state:', err); // Log the error
    res.status(500).json({ error: 'Error fetching dealerships by state' });
  }
});

// Express route to fetch dealer by a particular id
app.get('/fetchDealer/:id', async (req, res) => {
  const { id } = req.params; // Use the id variable
  try {
    // Replace this with actual code to fetch dealer by id
    res.json({ message: `Fetching dealer with ID ${id}` });
  } catch (err) {
    console.error('Error fetching dealer:', err); // Log the error
    res.status(500).json({ error: 'Error fetching dealer' });
  }
});

// Express route to insert a review
app.post('/insert_review', async (req, res) => {
  const data = req.body; // Properly get data from request body
  
  try {
    const documents = await find().sort({ id: -1 });
    let new_id = documents.length ? documents[0].id + 1 : 1; // Handle the case if no documents found

    const review = new Reviews({
      id: new_id,
      name: data.name,
      dealership: data.dealership,
      review: data.review,
      purchase: data.purchase,
      purchase_date: data.purchase_date,
      car_make: data.car_make,
      car_model: data.car_model,
      car_year: data.car_year,
    });

    const savedReview = await review.save();
    res.json(savedReview);
  } catch (err) {
    console.error('Error inserting review:', err); // Log the error
    res.status(500).json({ error: 'Error inserting review' });
  }
});

// Start the Express server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
