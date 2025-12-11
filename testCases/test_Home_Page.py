import pytest


@pytest.mark.order(2)
class Test_HomePage:
    def test_007_order_titlecheck(self,homepage_setup):
        print("Testcase to order details")
        self.hp = homepage_setup
        self.hp.order_details_fn()
        self.hp.driver.implicitly_wait(3)
        actual_title = self.hp.driver.title
        print("Actual title is:", actual_title)

        if actual_title == "Orders / nopCommerce administration":
            print("Test_006_titleCheck Passed")
            assert True
            self.hp.driver.save_screenshot(".\\Screenshots\\" + "Order_deatils_titlecheck.png")
        else:
            print("Test_006_titleCheck Failed")
            assert False

    def test_008_search_order(self,homepage_setup):
        self.hp=homepage_setup
        self.hp.order_details_fn()
        self.hp.driver.implicitly_wait(2)
        self.hp.order_search_fn()

