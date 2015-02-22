import sys
import os
import click
import zmq


class PublishServer(object):
    def __init__(self, input_reader, port, inflight_file, processed_file):
        self.input_reader = input_reader
        if str(inflight_file).startswith('/'):
            self.inflight_writer = open(inflight_file, 'w')
        else:
            self.inflight_writer = open(input_reader.name + inflight_file, 'w')
        if not str(processed_file).startswith('/'):
            processed_file = input_reader.name + processed_file
        if os.path.isfile(processed_file):
            self.processed = set([_.strip() for _ in open(processed_file)])
        else:
            self.processed = set()
        self.processed_writer = open(processed_file, 'a')
        self.initial_processed_count = len(self.processed)
        print 'Reading from %s.  In flight file: %s, Processed file: %s, Number already processed: %d' \
              % (input_reader.name, self.inflight_writer.name, self.processed_writer.name, self.initial_processed_count)
        context = zmq.Context()
        self.socket = context.socket(zmq.REP)
        self.socket.bind('tcp://*:%d' % port)
        self.in_fight_count = 0
        self.emitted_count = 0

    def _handle_recv(self):
        message = self.socket.recv()
        if message:
            self.processed.add(message)
            print ' P>(%d) %s' % (len(self.processed) - self.initial_processed_count, message)
            self.processed_writer.write(message + '\n')
            self.processed_writer.flush()
            self.in_fight_count -= 1

    def _read_lines(self):
        for line in (_.strip() for _ in self.input_reader):
            if line in self.processed:
                print 'A>', line
            else:
                self.inflight_writer.write(line + '\n')
                yield line

    def _publish(self, line):
        self.in_fight_count += 1
        self.emitted_count += 1
        print 'E>(%d) %s' % (self.emitted_count, line)
        self.socket.send(line)

    def run(self):
        for to_process in self._read_lines():
            self._handle_recv()
            self._publish(to_process)
        while self.in_fight_count > 0:
            self._handle_recv()
            self.socket.send('TERM')
        self.inflight_writer.close()
        self.processed_writer.close()


@click.command()
@click.argument('input_reader', type=click.File())
@click.option('--port', type=click.INT, default=12000)
@click.option('--inflight', default='.inflight')
@click.option('--processed', default='.processed')
def run_server(input_reader, port, inflight, processed):
    ps = PublishServer(input_reader, port, inflight, processed)
    ps.run()
