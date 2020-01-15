## A python unittest enhancer
Pysmine provide bdd capabilities to python unittest testing framework.
Pysmine is simply a set of decorator functions that can be used in your tests to provide bdd capabilitites.

No need to change current configurations
No need to use a separate test runner
Backwards compatibility
Failing test are easier to debug.

Finally an option to make testing enjoyable


### Installation
pip install pysmine

### Usage

Let's say we have the following function we want to test:
```def make_decision(hungry, food_in_freezer):
    if hungry and not food_in_freezer:
        return 'Buy Food!'

    if hungry and food_in_freezer:
        return 'Eat your Food!'

    if not hungry and food_in_freezer:
        return 'Do not eat!'

    if not hungry and not food_in_freezer:
        return 'Do not care!'
 ```

Using pysmine decorators you can test it the following way:

```
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
                def it_tells_to_not_eat_the_food(self):
                    self.assertEqual(make_decision(self.hungry, self.food_in_freezer), "Do not eat!")

            @when
            def there_is_not_food_in_the_freezer(self):
                self.food_in_freezer = False

                @it
                def tells_to_not_care(self):
                    self.assertEqual(make_decision(self.hungry, self.food_in_freezer), "Do not care!")
```
REMEMBER: If you want to pass values down to a nested test, assign that value to self.


## How does it work?

Before these tests run, the hierachy of tests is traversed and new tests are generated. This generated tests are the tests that actually run.

This is an example of a test that would be generated from the previous code:

```
def  test__I_am_hungry__there_is_food_in_the_freezer__tells_to_eat_the_food(self):
    I_am_hungry(self)
    there_is_food_in_the_freezer(self)
    tells_to_eat_the_food(self)
```


## Common Issues
### TypeError: arg 5 (closure) must be tuple
This is because you are trying to access a value in a parent scope. Remember that the only way to pass values to a nested test is to assign the value to the self object.