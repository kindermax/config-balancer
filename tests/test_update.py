import itertools

import pytest

import helpers


def test_update():
    config = {
        'ginger': {
            'django': 2,
            'flask': 3,
        },
        'cucumber': {
            'flask': 1,
        },
    }

    updated_config = helpers.update(config, 'pylons', 7)
    assert updated_config == {
        'ginger': {
            'django': 2,
            'flask': 3,
            'pylons': 1,
        },
        'cucumber': {
            'flask': 1,
            'pylons': 6,
        },
    }

def test_initial1_machines():
    config = {
        'ginger': {},
    }

    updated_config = helpers.update(config, 'flask', 3)
    updated_config = helpers.update(updated_config, 'django', 3)

    assert sum(sum(x.values()) for x in updated_config.values()) == 3 + 3


def test_initial2_mahines():
    config = {
        'ginger': {},
        'cucumber': {},
    }

    updated_config = helpers.update(config, 'flask', 3)
    updated_config = helpers.update(updated_config, 'django', 3)

    assert sum(updated_config['ginger'].values()) == sum(updated_config['cucumber'].values())
    assert sum(sum(x.values()) for x in updated_config.values()) == 3 + 3


def test_initial3_machines():
    config = {
        'machine1': {},
        'machine2': {},
        'machine3': {},
    }

    updated_config = helpers.update(config, 'flask', 3)
    updated_config = helpers.update(updated_config, 'django', 3)

    assert sum(sum(x.values()) for x in updated_config.values()) == 3 + 3



def test_update3_machines():
    config = {
        'machine1': {
            'django': 2,
            'flask': 3,
        },
        'machine2': {
            'flask': 1,
        },
        'machine3': {
            'flask': 1,
        },
    }

    updated_config = helpers.update(config, 'pylons', 7)
    assert updated_config == {
        'machine1': {
            'django': 2,
            'flask': 3,
        },
        'machine2': {
            'flask': 1,
            'pylons': 4,
        },
        'machine3': {
            'flask': 1,
            'pylons': 3,
        },
    }


def test_update4_machines():
    config = {
        'machine1': {
            'django': 2,
            'flask': 3,
        },
        'machine2': {
            'flask': 7,
        },
        'machine3': {
            'flask': 1,
        },
        'machine4': {
            'pylons': 3,

        },
    }

    updated_config = helpers.update(config, 'pylons', 7)
    assert updated_config == {
        'machine1': {
            'django': 2,
            'flask': 3,
            'pylons': 1,
        },
        'machine2': {
            'flask': 7,
        },
        'machine3': {
            'flask': 1,
            'pylons': 4,
        },
        'machine4': {
            'pylons': 5,

        },
    }


@pytest.mark.xfail(reason="Advanced test. Optional to implement")
def test_predictable_config():
    permutations = []
    services = [
        ('flask', 7),
        ('django', 13),
        ('pylons', 17)
    ]

    for permutation in itertools.permutations(services):
        config = {
            'ginger': {},
            'cucumber': {},
        }
        updated_config = dict(config)
        for svc, num in permutation:
            updated_config = helpers.update(updated_config, svc, num)
        print(updated_config)
        assert sum(sum(x.values()) for x in updated_config.values()) == 7 + 13 + 17
        permutations.append(updated_config)

    # check if first element equal with the rest of the elements
    assert all(p == permutations[0] for p in permutations[1:])
