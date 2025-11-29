# Group 15 Microservices
## Currency Conversion Microservice

### Installation

Install the required dependencies: pip install -r requirements.txt


### How to send a request

Write a conversiton command in the `request.txt` file. The command must follow this format: "convert: amount,from_currency,to_current". Notice there is no spaces bewteen commas, e.g "convert: 100,USD,EUR"

```python
with open('report.txt', 'w') as f:
    f.write("convert: 100,USD,EUR")
```


### How to receive the results 

Results can be read directly from the `request.txt` file.

```python
    with open('report.txt', 'r') as f:
        results = f.read()
    print(results)
```
