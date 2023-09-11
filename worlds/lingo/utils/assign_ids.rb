require 'set'
require 'yaml'

configpath = ARGV[0]
outputpath = ARGV[1]

next_item_id = 444400
next_location_id = 444400

old_generated = YAML.load_file(outputpath)
File.write(outputpath + ".old", old_generated.to_yaml)

if old_generated.include? "special_items" then
  old_generated["special_items"].each do |name, id|
    if id >= next_item_id then
      next_item_id = id + 1
    end
  end
end
if old_generated.include? "special_locations" then
  old_generated["special_locations"].each do |name, id|
    if id >= next_location_id then
      next_location_id = id + 1
    end
  end
end
if old_generated.include? "panels" then
  old_generated["panels"].each do |room, panels|
    panels.each do |name, id|
      if id >= next_location_id then
        next_location_id = id + 1
      end
    end
  end
end
if old_generated.include? "doors" then
  old_generated["doors"].each do |room, doors|
    doors.each do |name, ids|
      if ids.include? "location" then
        if ids["location"] >= next_location_id then
          next_location_id = ids["location"] + 1
        end
      end
      if ids.include? "item" then
        if ids["item"] >= next_item_id then
          next_item_id = ids["item"] + 1
        end
      end
    end
  end
end
if old_generated.include? "door_groups" then
  old_generated["door_groups"].each do |name, id|
    if id >= next_item_id then
      next_item_id = id + 1
    end
  end
end
if old_generated.include? "progression" then
  old_generated["progression"].each do |name, id|
    if id >= next_item_id then
      next_item_id = id + 1
    end
  end
end

door_groups = Set[]

config = YAML.load_file(configpath)
config.each do |room_name, room_data|
  if room_data.include? "panels"
    room_data["panels"].each do |panel_name, panel|
      unless old_generated.include? "panels" and old_generated["panels"].include? room_name and old_generated["panels"][room_name].include? panel_name then
        old_generated["panels"] ||= {}
        old_generated["panels"][room_name] ||= {}
        old_generated["panels"][room_name][panel_name] = next_location_id

        next_location_id += 1
      end
    end
  end

  if room_data.include? "doors"
    room_data["doors"].each do |door_name, door|
      if door.include? "event" and door["event"] then
        next
      end

      unless door.include? "skip_item" and door["skip_item"] then
        unless old_generated.include? "doors" and old_generated["doors"].include? room_name and old_generated["doors"][room_name].include? door_name and old_generated["doors"][room_name][door_name].include? "item" then
          old_generated["doors"] ||= {}
          old_generated["doors"][room_name] ||= {}
          old_generated["doors"][room_name][door_name] ||= {}
          old_generated["doors"][room_name][door_name]["item"] = next_item_id
  
          next_item_id += 1
        end

        if door.include? "group" and not door_groups.include? door["group"] then
          door_groups.add(door["group"])

          unless old_generated.include? "door_groups" and old_generated["door_groups"].include? door["group"] then
            old_generated["door_groups"] ||= {}
            old_generated["door_groups"][door["group"]] = next_item_id
    
            next_item_id += 1
          end
        end
      end

      unless door.include? "skip_location" and door["skip_location"] then
        unless old_generated.include? "doors" and old_generated["doors"].include? room_name and old_generated["doors"][room_name].include? door_name and old_generated["doors"][room_name][door_name].include? "location" then
          old_generated["doors"] ||= {}
          old_generated["doors"][room_name] ||= {}
          old_generated["doors"][room_name][door_name] ||= {}
          old_generated["doors"][room_name][door_name]["location"] = next_location_id
  
          next_location_id += 1
        end
      end
    end
  end

  if room_data.include? "progression"
    room_data["progression"].each do |progression_name, pdata|
      unless old_generated.include? "progression" and old_generated["progression"].include? room_name and old_generated["progression"][room_name].include? progression_name then
        old_generated["progression"] ||= {}
        old_generated["progression"][progression_name] = next_item_id

        next_item_id += 1
      end
    end
  end
end

File.write(outputpath, old_generated.to_yaml)
