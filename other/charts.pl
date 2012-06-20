#!/usr/bin/env perl
#
# File: charts.pl
# Author: Mathieu (matael) Gaborit
#       <mat.gaborit@gmx.com>
# Date: 2012
# License: WTFPL

use strict;
use warnings;
use SVG::TT::Graph::Bar;
use LWP::Simple;
use JSON;

sub generate_chart {
	# Please provide a base url, /api/all will be added next
	my $base = shift;
	my $chart_data = from_json(get("$base/api/all"));
	my $quotes = $chart_data->{results};

	my @fields;
	my @plot_data;
	foreach my $cur (@{$quotes}) {
		push @fields, $cur->[0];
		push @plot_data, $cur->[3]-$cur->[4];
	}

	my $graph  = SVG::TT::Graph::Bar->new({
		'height' 				=> '500',
		'width' 				=> '500',
		'fields' 				=> \@fields,
		'graph_title' 			=> 'Votes par quote',
		'show_graph_title' 		=> 1,
		'graph_subtitle' 		=> 'from quotes.matael.org',
		'show_graph_subtitle' 	=> 1,
		'scale_integers' 		=> 1
	});

	$graph->add_data({
		'data' 		=> \@plot_data,
		'title' 	=> 'Votes'
	});

	print $graph->burn();
}

generate_chart("http://quotes.example.org");
