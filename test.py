#!/usr/bin/env python3
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""A demo of the Google Assistant GRPC recognizer."""

import logging

import aiy.assistant.grpc
import aiy.audio
import aiy.voicehat
import aiy.cloudspeech

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
)


def main():
    aiy.i18n.set_language_code('fr-FR')
    print(aiy.i18n.get_language_code())
    status_ui = aiy.voicehat.get_status_ui()
    status_ui.status('starting')
    assistant = aiy.assistant.grpc.get_assistant()

    button = aiy.voicehat.get_button()
    led = aiy.voicehat.get_led()

    with aiy.audio.get_recorder():
        while True:
            status_ui.status('ready')
            print('Press the button and speak')
            button.wait_for_press()
            status_ui.status('listening')
            print('Listening...')
            text, audio = assistant.recognize()
            if text:
                if text == 'goodbye':
                    status_ui.status('stopping')
                    print('Bye!')
                    break
                elif text == 'blink':
                    led.set_state(aiy.voicehat.LED.BLINK)
                    break
                print('You said "', text, '"')
            if audio:
                aiy.audio.play_audio(audio)


if __name__ == '__main__':
    main()
