## Running grader locally

#### With [Docker Toolbox](https://docs.docker.com/toolbox/toolbox_install_mac/)
1. Navigate to project root dir:
```Bash
cd KotlinCourseraAssignments
```

2. Start docker-machine 
```Bash
docker-machine start
```

3. Set env vars for docker:
```Bash
eval "$(docker-machine env default)"
```
4. Build docker image:
```Bash
docker build -t kotlin_for_java_devs -f grader/Dockerfile .
```

5. Run with courseraprogramming tool:
SUMBIT - path to folder with single file submission.zip
PARTID - can be found in executeGrader.sh (ids are copied from Coursera)
```Bash
courseraprogramming grade local kotlin_for_java_devs <SUBMIT> partId <PARTID>
```

#### With [Docker for Mac](https://docs.docker.com/docker-for-mac/)
1. Set DOCKER_HOST env variable:
```
export DOCKER_HOST=unix:///var/run/docker.sock
```
2. Add change for courseraprogramming from the [fix](https://github.com/coursera/courseraprogramming/commit/318defc949b1dac22a85da9e4db7fb3c6103e6f3#diff-35937d256d503e689ce22b0107452960) that hasn't been rleased yet:
- Go to /Library/Frameworks/Python.framework/Versions/2.7/lib/python2.7/site-packages/courseraprogramming/utils.py#docker_client, line 138
- Change condition to ```not args.strict_docker_tls and 'tls' in kwargs```

3. Build docker image:
```Bash
docker build -t kotlin_for_java_devs -f grader/Dockerfile .
```

4. Run with courseraprogramming tool:
SUMBIT - path to folder with single file submission.zip
PARTID - can be found in executeGrader.sh (ids are copied from Coursera)
```Bash
courseraprogramming grade local kotlin_for_java_devs <SUBMIT> partId <PARTID>
```


More info can be found [here](https://github.com/coursera/programming-assignments-demo/tree/master/custom-graders)

## Updating grader to Coursera

Upload to Coursera grader prepared with the following command:
```bash
docker save kotlin_for_java_devs > kotlin_for_java_devs.v1.1.tar
```

## Extracting submission

Put the user submission in `submits/submission` and run:

```
python3 grader/prepare_solution.py submits/submission
```