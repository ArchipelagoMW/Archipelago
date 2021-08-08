#!/usr/bin/perl

# ips.pl
# version 0.01
#
# This is a quick hack to apply IPS patches. It is distributed under
# the terms of the GNU General Public License.

if (@ARGV != 1)
{
    print "manger"
}

open PAT, "$ARGV[0]" or die "Can't open $ARGV[1]";

read PAT, $data, 5;
die "Bad magic bytes in $ARGV[1]" if $data ne "PATCH";
printf("'%s': {", $ARGV[0]);
my $first = 1;
while(1)
{
    read PAT, $data, 3 or die "Read error";
    if ($data eq "EOF")
    {
	printf("},\n");
	exit;
    }
    if($first == 1) {
	$first = 2;
    } else {
	printf(",\n");
    }
    # This is ugly, but unpack doesn't have anything that's
    # very helpful for THREE-byte numbers.
    $address = ord(substr($data,0,1))*256*256 +
	ord(substr($data,1,1))*256 +
	ord(substr($data,2,1));

    read PAT, $data, 2 or die "Read error";
    $length = ord(substr($data,0,1))*256 + ord(substr($data,1,1));
    if ($length)
    {
	read(PAT, $data, $length) == $length or die "Read error";

	my @chars = split("", $data);

        printf ("0x%lX: [", $address);
	for(my $i=0; $i < $length; $i++) {
	    printf ("0x%lX", ord($chars[$i]));
	    if($i != $length - 1) {
		printf(",");
	    }
	    if(($i % 38) == 0 && $i != 0) {
		printf("\n");
	    }
	}
        printf ("]");
    }
    else # RLE mode
    {
	read PAT, $data, 2 or die "Read error";
	$length = ord(substr($data,0,1))*256 + ord(substr($data,1,1));
	read PAT, $byte, 1 or die "Read error";

        printf ("0x%lX: [", $address);
        for(my $i=0; $i < $length; $i++) {
	    printf ("0x%lX", ord($byte));
	    if($i != $length - 1) {
		printf(",");
	    }
	    if(($i % 38) == 0 && $i != 0) {
		printf("\n");
	    }
	}
        printf ("]");
    }
}
