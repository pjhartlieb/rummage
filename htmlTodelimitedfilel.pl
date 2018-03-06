#!/usr/bin/perl

############################################################
##
##		htmlTodelimitedfile.pl v0.0.1
##		
##		Convert html to delimited file
##
##		by pjhartlieb
##
############################################################

# This script will parse a specific html page and create a delimited file
# This is a horrible hack.  There must be a better way.

#import modules
use HTML::Element;
use Carp;
use WWW::Mechanize;
use HTML::TreeBuilder;
use LWP::UserAgent;
use HTML::Parse;
use List::MoreUtils qw(uniq);
use strict;
use warnings;
use Data::Dumper;
use HTML::Tree;
use LWP::Simple;
use Getopt::Long;

#initialize variables
my @kids;
my @list;

#parse the target html file
print "[*] Parsing target file \n";
print "\n";

my $filename = '<full_path_to_file>';	#specify the system file
open(my $target, $filename)		#read in the system file 
  or die "Could not open file '$filename' $!";

my $tree_main = HTML::Tree->new_from_file($target); 	#create new tree object

$tree_main->parse($target);	#populate tree object with parsed content from file

my @refItems = $tree_main->look_down( '_tag', 'dl' );	#create an array.  each element a the chunk  of code enclosed by the specified tag

#create a delimited entry for each string you are after. ugly ugly fucking hack.
##the elements within each code chunk are split out into an array @kids
##group and arrange them however
foreach my $node (@refItems) {
	@kids = $node->content_list();
	my ($p0,$p1,$p2,$p3,$p4,$p5,$p6,$p7,$p8,$p9);
		 (my $p00, my $p01) = @kids[0,1];
		 	if( defined $p00 ) {
				$p0= $p00->as_text;
			} else {
				$p0 = "undef";
			}
			if( defined $p01 ) {
				$p1= $p01->as_text;
			} else {
				$p1 = "undef";
			}
		 my $p0_1 = $p0.$p1;
		 
		 (my $p02, my $p03) = @kids[2,3];
		 	if( defined $p02 ) {
				$p2= $p02->as_text;
			} else {
				$p2 = "undef";
			}
			if( defined $p03) {
				$p3= $p03->as_text;
			} else {
				$p3 = "undef";
			}
		 my $p2_3 = $p2.$p3;
		 
		 (my $p04, my $p05) = @kids[4,5];
		 	if( defined $p04 ) {
				$p4= $p04->as_text;
			} else {
				$p4 = "undef";
			}
			if( defined $p05 ) {
				$p5= $p05->as_text;
			} else {
				$p5 = "undef";
			}
		 my $p4_5 = $p4.$p5;
		 
		 (my $p06, my $p07) = @kids[6,7];
		 	if( defined $p06 ) {
				$p6= $p06->as_text;
			} else {
				$p6 = "undef";
			}
			if( defined $p07 ) {
				$p7= $p07->as_text;
			} else {
				$p7 = "undef";
			}
		 my $p6_7 = $p6.$p7;
		 
		 (my $p08, my $p09) = @kids[8,9];
		 	if( defined $p08 ) {
				$p8= $p08->as_text;
			} else {
				$p8 = "undef";
			}
			if( defined $p09 ) {
				$p9= $p09->as_text;
			} else {
				$p9 = "undef";
			}
		 my $p8_9 = $p8.$p9;
		
	my $entry=$p1.";".$p3.";".$p5.";".$p7.";".$p9;	#choose items of interest. choose a delimiter.  Here its a ";"
	push (@list, $entry);	#push entry to array										
}

#write array to file
my $output_file='sanctioned.txt';
open(my $ofh, '>'.$output_file)
	or die "Could not open file '$output_file' $!";

foreach my $result (@list) {
	print $ofh $result,"\n";
}

close $ofh;

