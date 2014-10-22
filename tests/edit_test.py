# coding=utf-8
from selenium.webdriver.common.by import By
from tests.basic_testcase import BasePage
from tests.config import *
from tests.pages.page_object import CreateAdPage, CampaignsPage


class AdEditTestCase(BasePage):
    @classmethod
    def setUpClass(cls):
        super(AdEditTestCase, cls).setUpClass()
        ad_page = CreateAdPage(cls.driver)
        cls._fill_basic_settings(ad_page)

        sex_sex_sex = ad_page.sex_targeting
        sex_sex_sex.toggle_wrapper()  # opening
        for hot_hot_hot in sex_sex_sex.SEX_TARGETINGS.keys():
            chosen = sex_sex_sex.check_chosen([hot_hot_hot])
            if (chosen and not hot_hot_hot in TEST_SEX_DATA) or (not chosen and hot_hot_hot in TEST_SEX_DATA):  # It can be already allocated
                sex_sex_sex.toggle(hot_hot_hot)

        where_targeting = ad_page.where_targeting
        where_targeting.clear_all()
        for where in TEST_WHERE_DATA:
            where_targeting.toggle(REGIONS_ID[where])

        ad_page.banner_form.fill_banner(**BANNER_DATA)
        ad_page.submit_campaign()

        cls.editor = CampaignsPage(cls.driver).campaigns_list.get_campaign(CAMPAIGN_NAME).edit()

    @classmethod
    def tearDownClass(cls):
        campaigns_page.open()
        campaigns_page.campaigns_list.get_campaign(CAMPAIGN_NAME).delete()

    # @unittest.SkipTest
    def test_campaign_name_correct(self):
        """
            Проверка правильности имени кампании
        """
        name = self.editor.base_settings.get_campaign_name()
        self.assertEqual(CAMPAIGN_NAME, name)

    # @unittest.SkipTest
    def test_pad_correct(self):
        """
            Проверка правильности площадки
        """
        pad = self.editor.base_settings.get_pad()
        self.assertEqual(PAD_TYPE, pad)

    # @unittest.SkipTest
    def test_banner_preview_correct(self):
        """
            Проверка правильности данных в баннере
        """
        banner_preview = self.editor.banner_preview
        url = banner_preview.get_url()

        self.assertIn(BANNER_DATA['url'], url, "URL isn't correct")

    # @unittest.SkipTest
    def test_income_correct(self):
        """
            Проверяет то, что income был сохранен верно
        """
        income = self.editor.income_targeting
        text = income.get_header_text()

        income._toggle_settings()
        all_incomes_checked, not_checked = income.check_chosen_by_id(INCOME_TARGETINGS)

        self.assertEqual(text, IncomeTargeting.HEADER_SELECTED_TEXT, 'No feedback about his (her) actions')
        self.assertTrue(all_incomes_checked, 'Some of the incomes have not been checked: %s' % list_to_str(not_checked))

    # @unittest.SkipTest
    def test_dates_correct(self):
        """
            Проверяет то, что даты работы кампании были сохранены верно
        """
        campaign_time = self.editor.campaign_time
        campaign_time._toggle_settings()

        from_date, to_date = campaign_time.get_dates()

        self.assertEqual(FROM_DATE, from_date, 'From date is incorrect')
        self.assertEqual(TO_DATE, to_date, 'To date is incorrect')

    # @unittest.SkipTest
    def test_dates_delta_correct(self):
        """
            Проверяет то, что разница между днями посчитана верно
        """
        campaign_time = self.editor.campaign_time
        campaign_time._toggle_settings()

        delta = int(campaign_time.get_length_in_days())
        actual_delta = (TO_DATE - FROM_DATE).days + 1

        self.assertEqual(actual_delta, delta)