#!/usr/bin/env python3.9

#docker run --name somestory -e POSTGRES_PASSWORD=mysecretpassword -e POSTGRES_USER=secretuser -e POSTGRES_DB=history_today -d postgres
import configparser
import os
import docker
from docker import errors
import logging
import json
import sys

##############################################################################
# TODO 1. how to 146% save last time used container??? Lock file in the root?
# TODO 2. check if docker daemon is alive ???
##############################################################################

prj_root = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
cfg_path = os.path.join(prj_root, 'config/db.ini')
config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
if os.path.exists(cfg_path):
    config.read(cfg_path)
else:
    logging.error(f"No such file ---> {cfg_path}")
    sys.exit(1)


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")

try:
    docker_client = docker.APIClient(base_url='unix://var/run/docker.sock')
except errors.DockerException as ex:
    logging.error(f'Please check if docker started: systemctl status docker. Occurred -> {ex}')
    sys.exit(1)

try:
    db_image_id = ''

    try:
        logging.info('Here we are')
        logging.info(f"Looking for {config['CONTAINER_CONFIG']['image_name']}:{config['CONTAINER_CONFIG']['image_tag']}")
        for img in docker_client.images():
            if f"{config['CONTAINER_CONFIG']['image_name']}:{config['CONTAINER_CONFIG']['image_tag']}" in img['RepoTags']:
                db_image_id = img['Id']
                break
        # Check if is there the container with the name
        img_gen = docker_client.get_image(f"{config['CONTAINER_CONFIG']['image_name']}:{config['CONTAINER_CONFIG']['image_tag']}")
        f = next(img_gen)
    except errors.NotFound:
        logging.info(f"No image with tag {config['CONTAINER_CONFIG']['image_name']} found. Let's PULL it!")
        o = docker_client.pull(repository=config['CONTAINER_CONFIG']['image_name'], tag=config['CONTAINER_CONFIG']['image_tag'])
        if type(o) == str:
            logging.info(f"-> Pull of image {config['CONTAINER_CONFIG']['image_name']}")
        else:
            output = ''
            while True:
                try:
                    output = next(o)
                    json_output = json.loads(output)
                    if 'stream' in json_output:
                        print(json_output['stream'].strip('\n'))
                except StopIteration:
                    logging.info("Docker pulled")
                    break
                except ValueError:
                    logging.info("Error parsing output from docker image build: %s" % output)
    except KeyError:
        logging.error(f"Please check your config ---> {cfg_path}. There is no key {'CONTAINER_CONFIG'} or {'image_name'}")

    for cnt in docker_client.containers(all=True):
        if db_image_id in cnt['ImageID']:
            b = query_yes_no(f"Remove existing container {cnt['Id']} that based on image {config['CONTAINER_CONFIG']['image_name']}", "no")
            if b:
                logging.info(f'Removing container')
                docker_client.remove_container(cnt['Id'])

    db_container = docker_client.create_container(image=config['CONTAINER_CONFIG']['image_name'],
                                                  environment={'POSTGRES_USER': config['DB_CONFIG']['db_user'],
                                                               'POSTGRES_DB': config['DB_CONFIG']['db_name'],
                                                               'POSTGRES_PASSWORD': config['DB_CONFIG']['db_pwd']},
                                                  detach=True)
    docker_client.start(container=db_container.get('Id'))
    it = docker_client.attach(container=db_container.get('Id'),
                              stdout=True,
                              stderr=True,
                              stream=True,
                              logs=True)
    docker_logs_line = ''
    while True:
        try:
            docker_logs_line = next(it)
            print(docker_logs_line.decode('utf-8'))
        except StopIteration:
            break
except KeyboardInterrupt as e:
    logging.info(f'Stopping containers')
    for cnt in docker_client.containers(all=True):
        docker_client.stop(cnt['Id'])





