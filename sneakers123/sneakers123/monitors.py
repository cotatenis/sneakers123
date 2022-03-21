from spidermon import Monitor, MonitorSuite, monitors
from spidermon.contrib.actions.discord.notifiers import SendDiscordMessageSpiderFinished
from spidermon.contrib.monitors.mixins import StatsMonitorMixin
from sneakers123.actions import CloseSpiderAction
from spidermon.contrib.scrapy.monitors import FinishReasonMonitor, UnwantedHTTPCodesMonitor, ErrorCountMonitor

@monitors.name("Periodic job stats monitor")
class PeriodicJobStatsMonitor(Monitor, StatsMonitorMixin):
    @monitors.name("Maximum number of errors exceeded")
    def test_number_of_errors(self):
        accepted_num_errors = 5
        num_errors = self.data.stats.get("log_count/ERROR", 0)

        msg = "The job has exceeded the maximum number of errors"
        self.assertLessEqual(num_errors, accepted_num_errors, msg=msg)

@monitors.name('Item validation')
class ItemValidationMonitor(Monitor, StatsMonitorMixin):
    @monitors.name('No item validation errors')
    def test_no_item_validation_errors(self):
        validation_errors = getattr(
            self.stats, 'spidermon/validation/fields/errors', 0
        )
        self.assertEqual(validation_errors, 0, msg='Found validation errors in {} fields'.format(validation_errors))



class PeriodicMonitorSuite(MonitorSuite):
    monitors = [PeriodicJobStatsMonitor]
    monitors_failed_actions = [CloseSpiderAction, SendDiscordMessageSpiderFinished]


class SpiderCloseMonitorSuite(MonitorSuite):
    monitors = [ItemValidationMonitor, FinishReasonMonitor, UnwantedHTTPCodesMonitor, ErrorCountMonitor]

    monitors_failed_actions = [SendDiscordMessageSpiderFinished]