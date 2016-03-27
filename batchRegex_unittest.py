import unittest
from batchRegex import preprocess, postprocess


class TestPreprocessing(unittest.TestCase):

    def setUp(self):
        self.placeholder = r'<?rh-placeholder type="header" ?>'
        self.placeholder_exp = '<rh_placeholder type="header" />'
        self.x_condition = r'       <?rh-cbt_start condition="X_DO_NO_USE" ?><td style="border-right: Solid 1px #000000; '
        self.x_condition_exp = r'       <rh-cbt condition="X_DO_NO_USE"><td style="border-right: Solid 1px #000000; '
        self.end = r'       assistance when handling an interaction.</p></td><?rh-cbt_end ?>'
        self.end_exp = r'       assistance when handling an interaction.</p></td></rh-cbt>'

        self.all_conditions_pre = [
            (self.placeholder, self.placeholder_exp),
            (self.x_condition, self.x_condition_exp),
            (self.end, self.end_exp)
        ]

    def test_all_pre(self):
        for condition in self.all_conditions_pre:
            self.assertEqual(preprocess(condition[0]), condition[1])


class testPostProcessing(unittest.TestCase):

    def setUp(self):
        self.revertPlaceholder = r'<rh_placeholder type="header" />'
        self.revertPlaceholder_exp = r'<?rh-placeholder type="header" ?>'

        self.revertCondition = r'     <rh-cbt condition="X_DO_NO_USE"><td style="border-right: Solid 1px #000000; '
        self.revertCondition_exp = r'     <?rh-cbt_start condition="X_DO_NO_USE" ?><td style="border-right: Solid 1px #000000; '

        self.revertEnd = r'      assistance when handling an interaction.</p></td></rh-cbt>'
        self.revertEnd_exp = r'      assistance when handling an interaction.</p></td><?rh-cbt_end ?>'

        self.all_conditions_post = [
            (self.revertPlaceholder, self.revertPlaceholder_exp),
            (self.revertCondition, self.revertCondition_exp),
            (self.revertEnd, self.revertEnd_exp)
            ]

    def test_all_post(self):
        for condition in self.all_conditions_post:
            self.assertEqual(postprocess(condition[0]), condition[1])

if __name__ == "__main__":
    unittest.main()
