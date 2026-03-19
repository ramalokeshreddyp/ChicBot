# Evaluation Results

## Scoring Rubric

- **Relevance (1-5)**: How well does the response address the customer's query? (1 = Irrelevant, 5 = Perfectly relevant)
- **Coherence (1-5)**: Is the response grammatically correct and easy to understand? (1 = Incoherent, 5 = Flawless)
- **Helpfulness (1-5)**: Does the response provide a useful, actionable answer? (1 = Not helpful, 5 = Very helpful)

| Query # | Customer Query | Prompting Method | Response | Relevance (1-5) | Coherence (1-5) | Helpfulness (1-5) |
|---|---|---|---|---|---|---|
| 1 | "How do I track the shipping status of my recent order?" | Zero-Shot | You can track your order by logging into your account and visiting the 'Orders' section. There you will find a tracking number and a link to the carrier's website. | 5 | 5 | 5 |
| 1 | "How do I track the shipping status of my recent order?" | One-Shot | Hi there! You can easily track your order by visiting your 'Order History' page in your account. Just click on the tracking link provided next to your shipment. | 5 | 5 | 5 |
| 2 | "My discount code is not working at checkout." | Zero-Shot | Please ensure that the code is entered correctly and has not expired. Also, check if the items in your cart are eligible for the discount. | 4 | 5 | 4 |
| 2 | "My discount code is not working at checkout." | One-Shot | I'm sorry to hear that! Please double-check the spelling and expiration date. Some codes only apply to specific items. If it still fails, feel free to reach out! | 5 | 5 | 5 |
| 3 | "Can I change my shipping address after placing an order?" | Zero-Shot | Address changes are only possible if the order has not yet been processed. Please contact support immediately with your order number. | 5 | 5 | 5 |
| 3 | "Can I change my shipping address after placing an order?" | One-Shot | We can certainly try! If your order hasn't shipped yet, we can update the address. Please send us your order number as soon as possible. | 5 | 5 | 5 |
| 4 | "What is your policy on international shipping?" | Zero-Shot | We ship to most countries worldwide. Shipping costs and delivery times vary by location. Customs fees may apply. | 4 | 5 | 3 |
| 4 | "What is your policy on international shipping?" | One-Shot | We love our global customers! We offer international shipping to over 50 countries. Rates are calculated at checkout based on your location. | 5 | 5 | 4 |
| 5 | "I received a damaged item, how do I get a replacement?" | Zero-Shot | Please send a photo of the damaged item and your order number to our support email. We will process a replacement for you. | 5 | 5 | 5 |
| 5 | "I received a damaged item, how do I get a replacement?" | One-Shot | Oh no, I'm so sorry! Please email a photo of the damage to support@chicboutique.com, and we'll get a replacement sent out to you right away. | 5 | 5 | 5 |
| 6 | "How do I reset my account password?" | Zero-Shot | Go to the login page and click on 'Forgot Password'. Enter your email address to receive a reset link. | 5 | 5 | 5 |
| 6 | "How do I reset my account password?" | One-Shot | No problem! Just head to the login screen and click 'Forgot Password'. We'll send a reset link to your registered email address. | 5 | 5 | 5 |
| 7 | "Do you offer gift wrapping services?" | Zero-Shot | Yes, we offer gift wrapping for an additional fee. You can select this option during the checkout process. | 5 | 5 | 4 |
| 7 | "Do you offer gift wrapping services?" | One-Shot | We sure do! You can add gift wrapping to any order for just $5.00 during checkout. We'll even include a personalized note! | 5 | 5 | 5 |
| 8 | "How can I cancel my subscription?" | Zero-Shot | You can cancel your subscription in your account settings under the 'Subscriptions' tab. | 5 | 5 | 4 |
| 8 | "How can I cancel my subscription?" | One-Shot | We'll be sad to see you go! You can manage or cancel your subscription anytime through your account dashboard under 'My Subscriptions'. | 5 | 5 | 5 |
| 9 | "What payment methods do you accept?" | Zero-Shot | We accept major credit cards, PayPal, and Apple Pay. | 5 | 5 | 4 |
| 9 | "What payment methods do you accept?" | One-Shot | We accept all major credit cards, PayPal, and Apple Pay to make your shopping experience as smooth as possible! | 5 | 5 | 5 |
| 10 | "Is there a physical store I can visit?" | Zero-Shot | Currently, we are an online-only store and do not have any physical locations. | 4 | 5 | 4 |
| 10 | "Is there a physical store I can visit?" | One-Shot | We are strictly an online boutique at the moment, which allows us to bring you the best prices and latest styles directly! | 5 | 5 | 5 |
| 11 | "How do I use my store credit?" | Zero-Shot | Store credit can be applied at the checkout page. It will appear as a payment option if you are logged in. | 4 | 5 | 4 |
| 11 | "How do I use my store credit?" | One-Shot | Your store credit will automatically appear as a payment method at checkout! Just make sure you're logged into your account. | 5 | 5 | 5 |
| 12 | "Can I combine two separate orders into one shipment?" | Zero-Shot | We cannot guarantee that orders can be combined once they are placed, but you can contact support to check the status. | 4 | 5 | 3 |
| 12 | "Can I combine two separate orders into one shipment?" | One-Shot | Unfortunately, our system processes orders individually. However, if you contact us quickly, we'll see if our warehouse can help! | 4 | 5 | 4 |
| 13 | "What should I do if my package is marked as delivered but I haven't received it?" | Zero-Shot | Please check with your neighbors or local post office. If you still cannot find it, contact our support team. | 4 | 5 | 4 |
| 13 | "What should I do if my package is marked as delivered but I haven't received it?" | One-Shot | Sometimes carriers mark items early! Please wait 24 hours and check with neighbors. If it's still missing, let us know and we'll investigate. | 5 | 5 | 5 |
| 14 | "Are your products ethically sourced?" | Zero-Shot | We strive to work with suppliers who follow ethical labor practices. | 3 | 5 | 2 |
| 14 | "Are your products ethically sourced?" | One-Shot | Ethical sourcing is a priority for us! We partner with manufacturers who meet high standards for fair labor and sustainability. | 4 | 5 | 4 |
| 15 | "How do I unsubscribe from your newsletter?" | Zero-Shot | Click the 'Unsubscribe' link at the bottom of any of our emails. | 5 | 5 | 5 |
| 15 | "How do I unsubscribe from your newsletter?" | One-Shot | You can opt-out anytime by clicking the 'Unsubscribe' link at the bottom of our newsletters. We'll miss having you! | 5 | 5 | 5 |
| 16 | "Do you have a size guide for your clothing?" | Zero-Shot | Yes, a size guide is available on each product page next to the size selection. | 5 | 5 | 5 |
| 16 | "Do you have a size guide for your clothing?" | One-Shot | Definitely! You'll find a detailed 'Size Chart' link on every product page to help you find the perfect fit. | 5 | 5 | 5 |
| 17 | "Can I pre-order upcoming items?" | Zero-Shot | Pre-ordering is available for select items. These will be clearly marked on the product page. | 5 | 5 | 4 |
| 17 | "Can I pre-order upcoming items?" | One-Shot | Yes! Keep an eye out for the 'Pre-Order' button on upcoming collections. We'll ship them to you as soon as they arrive. | 5 | 5 | 5 |
| 18 | "How do I contact customer support via phone?" | Zero-Shot | Our phone support is available at 1-800-CHIC-BOU from 9 AM to 5 PM EST. | 4 | 5 | 5 |
| 18 | "How do I contact customer support via phone?" | One-Shot | We'd love to chat! You can reach our friendly team at 1-800-CHIC-BOU Monday through Friday, 9 AM - 5 PM EST. | 5 | 5 | 5 |
| 19 | "What happens if an item I ordered is out of stock?" | Zero-Shot | If an item is out of stock, we will notify you and issue a full refund for that item. | 5 | 5 | 5 |
| 19 | "What happens if an item I ordered is out of stock?" | One-Shot | If something you love is out of stock, we'll let you know immediately and provide a full refund or a similar alternative! | 5 | 5 | 5 |
| 20 | "Do you offer wholesale pricing for bulk orders?" | Zero-Shot | Yes, we offer wholesale pricing. Please contact our sales department for more information. | 4 | 5 | 4 |
| 20 | "Do you offer wholesale pricing for bulk orders?" | One-Shot | We do! For bulk inquiries, please reach out to wholesale@chicboutique.com with your business details and order volume. | 5 | 5 | 5 |
