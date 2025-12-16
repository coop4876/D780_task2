# D780_task2

### Ian Cooper - StudentID: 011018309 - Python 3.13.6

## Microservices Initialization

### Requirements

1. Python Version >= 3.8
2. Local Docker Installation

### Steps to run

1. run `docker compose up --build` from the project directory

## cart_service.py

cart_services.py handles the creation and update of user shopping carts.

### class CartUpdate

The CartUpdate class functions as a data model for the json request body that add_item expects. No user interaction is expected or required.

### add_item

#### Description

add_item checks if the specified user_id exists in the carts dict and creates an entry for the user if not. It then adds the json request body item and quantity to the users cart dict.\

#### Usage

add_item accepts an HTTP POST request with the user_id specified as a path parameter `/cart/{user_id}`. It expects a json body of the form: `{"item": "string", "quantity": 0}`

### get_cart

#### Description

get_cart fetches a specified user_id cart.

#### Usage

get_cart accepts an HTTP GET request with the user_id specified as a path parameter `/cart/{user_id}`

## inventory_service.py

inventory_services.py handles the application inventory. Inventory items exist in a dict where they can be retrieved or updated.

### class InventoryUpdate

The InventoryUpdate class functions as a data model for the json request body that add_item expects. No user interaction is expected or required.

### get_item

#### Description

get_item fetches the inventory details for a specified item. If the item is not found in the inventory, it returns a 404 error.

#### Usage

get_item accepts an HTTP GET request with the item name specified as a path parameter `/inventory/{item}`

### add_item

#### Description

add_item updates the inventory of a given item by adding the specified item quantity to the current stock of the item.\
It notifies any observers of the change in inventory.

#### Usage

add_item accepts an HTTP PUT request with the item name specified as a path parameter `/inventory/{item}`. It expects a json body of the form: `{"quantity": 0}`

### add_observer

#### Description

add_observer instantiates a new InventoryObserver object and adds it to the notification list for inventory changes.

#### Usage

add_observer accepts an HTTP PUT request with the observer_id specified as a path parameter `/inventory/observer/{observer_id}`

### class InventoryObserver

The inventoryObserver class instantiates a new observer. No user interaction is expected or required.

### notify

notify is a helper function for add_item and sends an inventory update message to an observer with updated inventory details. No user interaction is expected or required.

### notify_observers

notify_observers iterates through the observers list, calling notify on each observer. No user interaction is expected or required.

## payment_service.py

payment_services.py handles payment processing via Credit Card or PayPal

### class PaymentType

The PaymentType claa enumerates the available payment types. No user interaction is expected or required.

### class CheckoutDetails

The CheckoutDetails class functions as a data model for the json request body that the checkout functino expects. No user interaction is expected or required.

### class PaymentStrategy

The PaymentStrategy class functions as an abstract class for the different payment types. No user interaction is expected or required.

### class CreditCardPayment

the CreditCardPayment class processes payment via credit card. No user interaction is expected or required.

### pay

pay functions as a stand-in for processing a given payment type.

### class PayPalPayment

The PayPalPayment class processes payment via PayPal. No user interaction is expected or required.

### pay

pay functions as a stand-in for processing a given payment type.

### checkout

#### Description

The checkout function determines the submitted payment type, instantiates a class of the select strategy, and then processes the payent using the request body details.

#### Usage

checkout accepts an HTTP POST request with a json body in the form of `{"item": "string", "quantity": 0, "method": "string", "amount": 0}`. It returns the message specified in the payment method pay function.

## orchestrator_service.py

orchestrator_service.py functions as an orchestrator for the cart, inventory, and payment microservices. Docker URLs for each of the services are specified as global variables for the module.

### add_to_inventory

#### Description

add_to_inventory accesses the inventory api endpoint and adds the specified item and quantity.

#### Usage

add_to_inventory accepts an HTTP PUT request with the item name and quantity specified as query parameters.

### get_inventory

#### Description

get_inventory retrieves the inventory of a given item from the inventory api endpoint.

#### Usage

get_inventory accepts an HTTP GET request with the item name specified as a query parameter.

### process_payment

#### Description

process_payment processes the requested payment with the payment api endpoint.

#### Usage

process_payment accepts an HTTP POST request with item, quantity, method, and amount specified as query parameters.

### add_to_cart

#### Description

add_to_cart checks the inventory of a specified item and if sufficient stock exists, adds the item and quantity to the users cart. It then subtracts that item quantity from the items inventory stock.

#### Usage

add_to_cart accepts an HTTP POST request with user_id, item, and quantity specified as query parameters.
