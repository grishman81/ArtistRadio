from pathlib import Path

from src.radio.scheduler import RadioScheduler



def test_scheduler_queue():

    scheduler = RadioScheduler()


    track = type(
        "Track",
        (),
        {
            "path": Path(
                "test.mp3"
            )
        },
    )()


    scheduler.add(
        track
    )


    assert scheduler.size() == 1


    result = scheduler.next()


    assert result.path == Path(
        "test.mp3"
    )


    assert scheduler.size() == 0