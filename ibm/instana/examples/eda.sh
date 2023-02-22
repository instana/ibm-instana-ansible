export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib/jvm/java-17-openjdk-17.0.6.0.10-3.el8_7.x86_64/lib/server
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-17.0.6.0.10-3.el8_7.x86_64/jre
ansible-rulebook --rulebook instana_event_rulebook.yml  -i inventory.yml --verbose
