![Image of Pysmine](https://i.ibb.co/d5bQ4Tg/logo.png)

# A Python Unittest Enhancer

Pysmine is simply a set of decorator functions that provide Behavior Driven Development capabilities to python unittest testing framework or pytest.

## Benefits
All Behavior Driven Development benefits.  
No need to change current configurations.  
No need to use a separate test runner.  
Light-weight.  

## Installation
```
pip install pysmine
```

## Decorators
`@with_nested_specs`: used on the test class.  
`@describe`: used to describe the unit to be tested.  
`@when`: used to add context to the test.  
`@it`: used to describe the expected behaviour.  

## Usage
Let's say we have the following function we want to test:
``` python
def make_decision(hungry, food_in_freezer):
    if hungry and not food_in_freezer:
        return 'Buy Food!'

    if hungry and food_in_freezer:
        return 'Eat your Food!'

    if not hungry and food_in_freezer:
        return 'Do not eat!'

    if not hungry and not food_in_freezer:
        return 'Do not care!'
 ```
 
This function has many different expected outputs depending on its arguments. A clean way to test this in a readable form using Pysmine decorators would be the following:

``` python
import unittest import TestCase
from pysmine import with_nested_specs, describe, when, it

@with_nested_specs
class TestExample(TestCase):

    @test
    def it_is_true(self):
        self.assertTrue(True)

    @describe
    def function_make_decision(self):

        @when
        def I_am_hungry(self):
            self.hungry = True

            @when
            def there_is_food_in_the_freezer(self):
                self.food_in_freezer = True

                @it
                def tells_to_eat_the_food(self):
                    self.assertEqual(make_decision(self.hungry, self.food_in_freezer), "Eat your Food!")
                
                @it
                def returns_a_string(self):
                    self.assertEqual(type(make_decision(self.hungry, self.food_in_freezer)), str)

            @when
            def there_is_not_food_in_the_freezer(self):
                self.food_in_freezer = False

                @it
                def tells_to_buy_food(self):
                    self.assertEqual(make_decision(self.hungry, self.food_in_freezer), "Buy Food!")

        @when
        def I_am_not_hungry(self):
            self.hungry = False

            @when
            def there_is_food_in_the_freezer(self):
                self.food_in_freezer = True

                @it
                def tells_to_not_eat_the_food(self):
                    self.assertEqual(make_decision(self.hungry, self.food_in_freezer), "Do not eat!")

            @when
            def there_is_not_food_in_the_freezer(self):
                self.food_in_freezer = False

                @it
                def tells_to_not_care(self):
                    self.assertEqual(make_decision(self.hungry, self.food_in_freezer), "Do not care!")
```

Just run the tests as you normally would and let the magic happen.


## How does it work?

Before these tests run, the hierachy of tests is traversed and new tests are generated. This generated tests are the tests that actually run.

An example of a test that would be generated from the example would be the following:

``` python
def test__I_am_hungry__there_is_food_in_the_freezer__tells_to_eat_the_food(self):
    I_am_hungry(self)
    there_is_food_in_the_freezer(self)
    tells_to_eat_the_food(self)
```

As you can see, it is basically calling every child individually with `self` passed as an argument. This means `self` should be used in order to pass values between the functions that compose the test.


## Common Issues
### TypeError: arg 5 (closure) must be tuple
This is because you are trying to access a value defined in a parent scope. Remember that the only way to pass values to a from the functions that compose a nested test is to assign the value to the `self` object.
