# Tagging AWS EC2 snapshots
To tag AWS EC2 snapshots after their originating volumes tags

Run this Python3 simple script to pass the volumes tags to their snapshots:\
 1- It gets all the snapshots ids in each listed region\
 2- Creates a list of existing volume ids\
 3- Gets the origin volume for each snapshot\
 4- If the volume still exists( is listed in step 2) then gets the volume tags and pass them to the snapshot
