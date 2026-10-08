from assessment.libs.dig import Dig

def describe_dig():
    basket = {
        "drinks": {
            "soft": {
                "coca-cola": 10,
                "sprite": 8,
            },
            "alcoholic": {
                "jack-daniels": 2
            }
        },
        "bakery": {
            "bagel": 7,
            "jam doughnut": 2
        }
    }

    def context_with_no_keys():

        def it_returns_data():
            basket = { 'orange': 1, 'banana': 3 }

            result = Dig.dig(basket)
            assert result == basket

    def describe_data_type():

        def context_when_not_a_dictionary():

            def it_returns_None():
                result = Dig.dig("data", "orange")
                assert result == None

        def context_when_its_a_dictionary():

            def context_when_it_has_keys():

                def it_returns_value_of_given_keys():

                    result = Dig.dig(basket, "drinks", "soft", "sprite")
                    assert result == 8

                def describe_default_output():

                    def context_when_keys_do_not_exist():

                        def context_with_given_default():
                            
                            def it_returns_given_default():
                                result = Dig.dig(basket, "confectionary", default=[])
                                assert result == []

                        def context_without_given_default():

                            def it_returns_defined_default():
                                result = Dig.dig(basket, "confectionary")
                                assert result == None
