/*
    Core logic/payment flow for this comes from here:
    https://stripe.com/docs/payments/accept-a-payment
    CSS from here: 
    https://stripe.com/docs/stripe-js
*/

// Initialize the keys from the json template filters in html
var stripe_public_key = $('#id_stripe_public_key').text().slice(1, -1);
var client_secret = $('#id_client_secret').text().slice(1, -1);
// With these keys we can set up Stripe (thanks to js included in base template )
var stripe = Stripe(stripe_public_key);
// Then initialize an instance of Stripe elements
var elements = stripe.elements();
// Before creating the card we must have predefined the style element for use
var style = {
    base: {
        color: '#000',
        fontFamily: '"Helvetica Neue", Helvetica, sans-serif',
        fontSmoothing: 'antialiased',
        fontSize: '16px',
        '::placeholder': {
            color: '#aab7c4'
        }
    },
    invalid: {
        color: '#dc3545',
        iconColor: '#dc3545'
    }
};
// Use this to create a card element
var card = elements.create('card', {style: style});

// Mount card element to a div present in checkout.html
card.mount('#card-element');
