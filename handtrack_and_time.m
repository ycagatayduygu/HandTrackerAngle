% Create a UDP object to receive data on port 12345.
% works with the hand_track_and_time_python.py. We are trying to send also
% time information to do a delay analysis
clear all
% Create a UDP object to receive data on port 12345.
u = udpport("LocalPort", 12345);

% Initialize arrays to store received angles, timestamps, and delays
receivedAngles = [];
receivedTimestamps = [];
delays = [];

% Initialize a counter for data received each second
dataPerSecond = 0;
lastSecondCheck = tic; % Start a timer

% Main loop to continuously read data
while true
    % Check if data is available
    if u.NumBytesAvailable > 0
        % Read the data received on the UDP port
        data = readline(u);
        
        % Process the data if it's not empty
        if ~isempty(data)
            % Split the received data into angle and timestamp
            parts = strsplit(data, ',');
            if numel(parts) == 2
                angle = str2double(parts{1});
                timestampPython = str2double(parts{2}); % Timestamp from Python
                
                % Append data to arrays
                receivedAngles(end+1) = angle;
                receivedTimestamps(end+1) = timestampPython;
                
                % Calculate delay
                currentTimestampMATLAB = posixtime(datetime('now','TimeZone','UTC')) * 1000; % Current time in milliseconds
                delay = currentTimestampMATLAB - timestampPython; % Delay in milliseconds
                delays(end+1) = delay;
                
                % Increment the counter
                dataPerSecond = dataPerSecond + 1;
                
                % Display angle and delay
                fprintf('Angle: %.2f degrees, Delay: %.2f ms\n', angle, delay);
            end
        end
    end
    
    % Check and print data received every second
    if toc(lastSecondCheck) >= 1
        fprintf('Data received in the last second: %d\n', dataPerSecond);
        dataPerSecond = 0; % Reset counter
        lastSecondCheck = tic; % Restart the timer
    end
    
    pause(0.01); % Small pause to prevent overwhelming CPU
end
