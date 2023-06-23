import pytest
import subprocess
import docker

import tarfile
from io import BytesIO
import random

# create docker client
client = docker.from_env()


def start_services():
    print("Starting services...")
    subprocess.check_call(['docker-compose', 'up', '-d'])

    # DEBUG
    # Get a list of running containers
    running_containers = client.containers.list()

    for container in running_containers:
        print(container.id)
        print(container.name)


def stop_services():
    print("Stopping services...")
    subprocess.check_call(['docker-compose', 'down'])


@pytest.fixture(scope="module", autouse=True)
def manage_services():
    start_services()
    yield
    stop_services()


def read_file(service_name, file_name):
    container = client.containers.get(service_name)

    file_archive = container.get_archive(file_name)
    stream, stat = file_archive
    file_obj = BytesIO()
    for i in stream:
        file_obj.write(i)
    file_obj.seek(0)
    tar = tarfile.open(mode='r', fileobj=file_obj)
    text = tar.extractfile('events.log')
    return text.read().decode('utf-8')


def read_logs(service_name):  # container-level logs
    print(f"Reading logs from {service_name}...")
    container = client.containers.get(service_name)
    print(str(container))
    logs = container.logs(stdout=True, stderr=False)  # 1st, cut
    # container-level log gives output like 'My hostname is: a9d3519b71f0\nworking as target\noutputfile events.log\nApp listening on port 9997\nclient connected\n'
    return logs.decode('utf-8')


def test_logs(manage_services):
    time.sleep(10)
    event_log1 = read_file('nodeecosystsm_target_1_1',
                           '/usr/src/app/events.log')  # container naming convention is different at this level than inside docker-compose
    event_log2 = read_file('nodeecosystsm_target_2_1', '/usr/src/app/events.log')
    # print(event_log1)

    event_log1 += '\n'  # ensure each log is newline terminated
    event_log2 += '\n'

    # Assuming the set of events is "large" - meaning too big to verify all data (not really the case here)
    # Apply boundary testing, test for the presence of first and last elements,
    # and a random sampling of in-between elements
    random_integers = [random.randint(2, 999999) for _ in range(98)]
    test_integers = [1, 1000000] + random_integers

    print("Testing event entries: " + str(test_integers))

    for test_num in test_integers:
        phrase = "This is event number " + str(test_num) + "\n"  # match newlines too, to avoid partial digit matches
        assert (phrase in event_log1) or (
                    phrase in event_log2)  # Verify that agent events are stored in 1 of the two targets

        if phrase in event_log1:  # Verify that splitter is not acting as a duplicator
            assert phrase not in event_log2
        else:
            assert phrase in event_log2

    print("Test completed successfully.")
