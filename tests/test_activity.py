import unittest
from activity import ActivityState


class ActivityTests(unittest.TestCase):
    def test_priority_and_return_to_underlying_state(self):
        s=ActivityState()
        s.key(10)
        self.assertEqual(s.state(10),'typing')
        s.sample(microphone=False,music=True,now=10)
        self.assertEqual(s.state(10),'typing')
        s.sample(microphone=False,music=True,now=10.6)
        self.assertEqual(s.state(10.6),'music')
        s.sample(microphone=True,music=True,now=11)
        s.sample(microphone=True,music=True,now=11.6)
        self.assertEqual(s.state(11.6),'microphone')
        self.assertEqual(s.state(11.6,usage_open=True),'usage')
        s.sample(microphone=False,music=True,now=12)
        self.assertEqual(s.state(12),'microphone')
        s.sample(microphone=False,music=True,now=13.6)
        self.assertEqual(s.state(13.6),'music')

    def test_short_spikes_and_missing_signal_do_not_stick(self):
        s=ActivityState()
        s.sample(True,False,now=1)
        s.sample(False,False,now=1.1)
        self.assertEqual(s.state(2),'idle')
        s.key(3)
        self.assertEqual(s.state(4),'typing')
        self.assertEqual(s.state(5),'idle')
        s.sample(True,True,now=6);s.sample(True,True,now=7)
        self.assertEqual(s.state(7),'microphone')
        self.assertEqual(s.state(15),'idle')  # stale detector can't pin activity forever


if __name__=='__main__':unittest.main()
