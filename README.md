http://localhost:4040
https://unaltered-eagle-wackiness.ngrok-free.dev/predict

Các endpoint public:

- `/docs`
- `/health`
- `POST /predict`

{
"brand": "Honda",
"car_age": 2,
"mileage_km": 45000.0,
"fuel_type": "Gasoline",
"transmission": "Automatic",
"condition": "Good"
}

200
{
"status": "success",
"input_summary": {
"brand": "Honda",
"car_age": 2,
"mileage_km": 45000,
"fuel_type": "Gasoline",
"transmission": "Automatic",
"condition": "Good"
},
"prediction": "DAT",
"probabilities": {
"Dat": "98.0%",
"Re": "2.0%"
}
}
