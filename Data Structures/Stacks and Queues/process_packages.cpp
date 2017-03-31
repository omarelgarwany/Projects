#include <iostream>
#include <queue>
#include <vector>

struct Request {
    Request(int arrival_time, int process_time):
        arrival_time(arrival_time),
        process_time(process_time)
    {}

    int arrival_time;
    int process_time;
};

struct Response {
    Response(bool dropped, int start_time):
        dropped(dropped),
        start_time(start_time)
    {}

    bool dropped;
    int start_time;
};

class Buffer {
public:
    Buffer(int size):
        size_(size),
        finish_time_()
    {}
    void clean_queue(const Request &request) {
        while (!(this->finish_time_).empty() && request.arrival_time >= (this->finish_time_).front()) {
            (this->finish_time_).pop();
        }
    }
    int compute_start_time (const Request &request) {
        int start_time = 0;
        if (!(this->finish_time_).empty()) {
            start_time += (this->finish_time_).back();
        } else {
            start_time += request.arrival_time;            
        }
        return start_time;        
    }
    int compute_finish_time(int start_time, const Request &request) {
        return start_time + request.process_time;
    }
    int compute_free_buffer_size() {
        int free_buffer_space = this->size_;
        if (!(this->finish_time_).empty()) {
            free_buffer_space -= (this->finish_time_).size();
        }
        return free_buffer_space;

    }
    Response Process(const Request &request) {
        // write your code here
        this->clean_queue(request);
        if ( !this->compute_free_buffer_size() ) return Response(true, -1);
        int start_time = this->compute_start_time(request);
        int finish_time = this->compute_finish_time(start_time, request);
        (this->finish_time_).push(finish_time);
        return Response(false, start_time);
    }
private:
    int size_;
    std::queue <int> finish_time_;
};

std::vector <Request> ReadRequests() {
    std::vector <Request> requests;
    int count;
    std::cin >> count;
    for (int i = 0; i < count; ++i) {
        int arrival_time, process_time;
        std::cin >> arrival_time >> process_time;
        requests.push_back(Request(arrival_time, process_time));
    }
    return requests;
}

std::vector <Response> ProcessRequests(const std::vector <Request> &requests, Buffer *buffer) {
    std::vector <Response> responses;
    for (int i = 0; i < requests.size(); ++i)
        responses.push_back(buffer->Process(requests[i]));
    return responses;
}

void PrintResponses(const std::vector <Response> &responses) {
    for (int i = 0; i < responses.size(); ++i)
        std::cout << (responses[i].dropped ? -1 : responses[i].start_time) << std::endl;
}

int main() {
    int size;
    std::cin >> size;
    std::vector <Request> requests = ReadRequests();

    Buffer buffer(size);
    std::vector <Response> responses = ProcessRequests(requests, &buffer);

    PrintResponses(responses);
    return 0;
}
