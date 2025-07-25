require 'roda'
require 'simdjson'
require 'fileutils'

DB_FILE = '/app/data/permissions.json'
FileUtils.mkdir_p('/app/data')
File.write(DB_FILE, '{}') unless File.exist?(DB_FILE)

def read_db
  content = File.read(DB_FILE)
  Simdjson.parse(content)
rescue Simdjson::ParseError, Errno::ENOENT
  {}
end

def write_db(data)
  File.write(DB_FILE, data.to_json)
end

class PermissionManager < Roda
  plugin :json

  route do |r|
    r.root do
      { status: "healthy", timestamp: Time.now.to_i }
    end

    r.post "create" do
      begin
        
        parsed_data = Simdjson.parse(r.body.read)
        uuid = parsed_data['uuid']

        if uuid.nil? || uuid.empty?
          response.status = 400
          next { error: "UUID is required" }
        end

        db = read_db
        if db.key?(uuid)
          response.status = 409
          next { error: "User already exists" }
        end

        db[uuid] = parsed_data.reject { |k, _| k == 'uuid' }
        write_db(db)
        { success: true, message: "User created successfully", uuid: uuid }
      rescue Simdjson::ParseError
        response.status = 400
        { error: "Invalid JSON format" }
      rescue => e
        response.status = 500
        { error: "Server error: #{e.message}" }
      end
    end

    r.get "fetch_perms" do
      uuid = r.params['uuid']
      if uuid.nil? || uuid.empty?
        response.status = 400
        next { error: "UUID parameter is required" }
      end

      db = read_db
      if db.key?(uuid)
        db[uuid]
      else
        response.status = 404
        { error: "User not found" }
      end
    end
  end
end