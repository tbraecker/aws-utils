# emr_instance_hours

We schedule this script to run periodically to make sure we dont have any long running clusters.
It pushes the NormalizedInstanceHours metric to Cloudwatch where we set an alarm on it.

If you want to use this you need to provide a Clustergroup-Tag (<YOUR TAG> in the script) because our clusters are grouped by tags
and a Cloudwatch Namespace (<YOUR NAMESPACE> in script)
