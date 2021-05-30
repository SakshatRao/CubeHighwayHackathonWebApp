# AI-Boosted Online Ordering for CubeStops
## Django-based Web Application proposal for Cube Highway Hackathon 2021
<br></br>

### Demo: https://www.youtube.com/watch?v=6KZ1Z1YzDso
#### Watch a short demonstration of the website!

<br>

### Website: https://online-ordering-cubestop.herokuapp.com/
#### Feel free to sign-up and explore the website!

<br></br>

## Features:
* **Virtual Menu**: I developed a simple frontend to order food items from a menu and place a order. Customers can view details, ratings, price and feedback for all food items and also apply coupons or reservation charges while finalizing the order.
* **Virtual Waiter**: Virtual Waiter is basically the Recommendation System which suggests food items for the customers to try based on their previous order history. To make these recommendations, I firstly calculate 'ingredient embeddings', similar to word embeddings in NLP. I trained a neural network to predict a food item's cuisine (South Indian, Bengali, etc.), category (starters, desserts, etc.) and taste (sweet, spicy, etc.) from its ingredients. I then obtain the ingredient embeddings from the weights of the neural network. Thus, I am able to represent a food item as the average of its ingredient embeddings and recommend food items which are closest to a customer's preferred taste. 
* **Quick Feedback**: Innovative approach to motivate customers to give their feedback by simply clicking a picture and giving a rating, that's it! The food item in the picture can be automatically detected by my CNN model in the background which reduces the amount of effort customers have to put to give feedback.
* **Incentives**: CubeStop Membership Discounts and Lucky-draw Discount Coupons upon order/feedback completion to incentivize customers to come back!
