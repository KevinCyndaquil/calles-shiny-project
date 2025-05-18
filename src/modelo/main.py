import street_model as model


def main():
    model.load_models()

    forecast = model.predict('AUTOS', 1)

    print(forecast[['ds', 'yhat']].tail(3))

    return 0

if __name__ == '__main__':
    main()