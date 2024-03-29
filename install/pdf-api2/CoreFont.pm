#=======================================================================
#    ____  ____  _____              _    ____ ___   ____
#   |  _ \|  _ \|  ___|  _   _     / \  |  _ \_ _| |___ \
#   | |_) | | | | |_    (_) (_)   / _ \ | |_) | |    __) |
#   |  __/| |_| |  _|    _   _   / ___ \|  __/| |   / __/
#   |_|   |____/|_|     (_) (_) /_/   \_\_|  |___| |_____|
#
#   A Perl Module Chain to faciliate the Creation and Modification
#   of High-Quality "Portable Document Format (PDF)" Files.
#
#   Copyright 1999-2005 Alfred Reibenschuh <areibens@cpan.org>.
#
#=======================================================================
#
#   THIS LIBRARY IS FREE SOFTWARE; YOU CAN REDISTRIBUTE IT AND/OR
#   MODIFY IT UNDER THE TERMS OF THE GNU LESSER GENERAL PUBLIC
#   LICENSE AS PUBLISHED BY THE FREE SOFTWARE FOUNDATION; EITHER
#   VERSION 2 OF THE LICENSE, OR (AT YOUR OPTION) ANY LATER VERSION.
#
#   THIS FILE IS DISTRIBUTED IN THE HOPE THAT IT WILL BE USEFUL,
#   AND ANY EXPRESSED OR IMPLIED WARRANTIES, INCLUDING, BUT NOT 
#   LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND 
#   FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT 
#   SHALL THE AUTHORS AND COPYRIGHT HOLDERS AND THEIR CONTRIBUTORS 
#   BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, 
#   EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT 
#   LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS 
#   OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
#   CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, 
#   STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) 
#   ARISING IN ANY WAY OUT OF THE USE OF THIS FILE, EVEN IF 
#   ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
#   SEE THE GNU LESSER GENERAL PUBLIC LICENSE FOR MORE DETAILS.
#
#   YOU SHOULD HAVE RECEIVED A COPY OF THE GNU LESSER GENERAL PUBLIC
#   LICENSE ALONG WITH THIS LIBRARY; IF NOT, WRITE TO THE
#   FREE SOFTWARE FOUNDATION, INC., 59 TEMPLE PLACE - SUITE 330,
#   BOSTON, MA 02111-1307, USA.
#
#   $Id: CoreFont.pm,v 2.0 2005/11/16 02:18:14 areibens Exp $
#
#=======================================================================
package PDF::API2::Resource::Font::CoreFont;

=head1 NAME

PDF::API2::Resource::Font::CoreFont - Module for using the 14 PDF built-in Fonts.

=head1 SYNOPSIS

    #
    use PDF::API2;
    #
    $pdf = PDF::API2->new;
    $cft = $pdf->corefont('Times-Roman');
    #

=head1 METHODS

=over 4

=cut

BEGIN {

    use utf8;
    use Encode qw(:all);

    use File::Basename;

    use vars qw( @ISA $fonts $alias $subs $encodings $VERSION );
    use PDF::API2::Resource::Font;
    use PDF::API2::Util;
    use PDF::API2::Basic::PDF::Utils;

    @ISA=qw(PDF::API2::Resource::Font);

    ( $VERSION ) = sprintf '%i.%03i', split(/\./,('$Revision: 2.0 $' =~ /Revision: (\S+)\s/)[0]); # $Date: 2005/11/16 02:18:14 $

}
no warnings qw[ deprecated recursion uninitialized ];

=item $font = PDF::API2::Resource::Font::CoreFont->new $pdf, $fontname, %options

Returns a corefont object.

=cut

=pod

Valid %options are:

I<-encode>
... changes the encoding of the font from its default.
See I<perl's Encode> for the supported values.

I<-pdfname> ... changes the reference-name of the font from its default.
The reference-name is normally generated automatically and can be
retrived via $pdfname=$font->name.

=cut

sub _look_for_font ($) 
{
    my $fname=shift;
    ## return(%{$fonts->{$fname}}) if(defined $fonts->{$fname});
    eval "require PDF::API2::Resource::Font::CoreFont::$fname; ";
    unless($@)
    {
    no strict 'refs';
        my $obj = "PDF::API2::Resource::Font::CoreFont::".$fname;
    $fonts->{$fname} = deep_copy(${$obj."::FONTDATA"});
        $fonts->{$fname}->{uni}||=[];
        foreach my $n (0..255) 
        {
            $fonts->{$fname}->{uni}->[$n]=uniByName($fonts->{$fname}->{char}->[$n]) unless(defined $fonts->{$fname}->{uni}->[$n]);
        }
        return(%{$fonts->{$fname}});
    } 
    else 
    {
        die "requested font '$fname' not installed ";
    }
}

#
# Deep copy something, thanks to Randal L. Schwartz
# Changed to deal w/ CODE refs, in which case it doesn't try to deep copy
#
sub deep_copy
{
    my $this = shift;
    if (not ref $this) 
    {
    $this;
    } 
    elsif (ref $this eq "ARRAY") 
    {
    [map &deep_copy($_), @$this];
    } 
    elsif (ref $this eq "HASH") 
    {
    +{map { $_ => &deep_copy($this->{$_}) } keys %$this};
    } 
    elsif (ref $this eq "CODE") 
    {
    # Can't deep copy code refs
    return $this;
    } 
    else 
    { 
    die "what type is $_?";
    }
}

sub _look_for_fontfile ($) 
{
    my $fname=shift;
    my $fpath=undef;
    foreach my $dir (@INC) 
    {
        $fpath="$dir/PDF/API2/Resource/Font/CoreFont/$fname";
        last if(-f $fpath);
        $fpath=undef;
    }
    return($fpath);
}

sub _look_for_fontmetricfile ($) 
{
    my $fname=shift;
    my $fpath=undef;
    foreach my $dir (@INC) 
    {
        $fpath="$dir/PDF/API2/Resource/Font/CoreFont/$fname.fm";
        last if(-f $fpath);
        $fpath=undef;
    }
    return($fpath);
}

sub new 
{
    my ($class,$pdf,$name,@opts) = @_;
    my ($self,$data);
    my %opts=();
    if(-f $name) 
    {
        eval "require '$name'; ";
        $name=basename($name,'.pm');
    }
    my $lookname=lc($name);
    $lookname=~s/[^a-z0-9]+//gi;
    %opts=@opts if((scalar @opts)%2 == 0);
    $opts{-encode}||='asis';

    $lookname = defined($alias->{$lookname}) ? $alias->{$lookname} : $lookname ;

    if(defined $subs->{$lookname}) 
    {
        $data={_look_for_font($subs->{$lookname}->{-alias})};
        foreach my $k (keys %{$subs->{$lookname}}) 
        {
            next if($k=~/^\-/);
            $data->{$k}=$subs->{$lookname}->{$k};
        }
    } 
    else 
    {
        unless(defined $opts{-metrics}) 
        {
            $data={_look_for_font($lookname)};
        } 
        else 
        {
            $data={%{$opts{-metrics}}};
        }
    }

    die "Undefined Font '$name($lookname)'" unless($data->{fontname});

    # we have data now here so we need to check if
    # there is a -ttfile or -afmfile/-pfmfile/-pfbfile
    # and proxy the call to the relevant modules
    #
    #if(defined $data->{-ttfile} && $data->{-ttfile}=_look_for_fontfile($data->{-ttfile})) 
    #{
    #    return(PDF::API2::Resource::CIDFont::TrueType->new($pdf,$data->{-ttfile},@opts));
    #} 
    #elsif(defined $data->{-pfbfile} && $data->{-pfbfile}=_look_for_fontfile($data->{-pfbfile})) 
    #{
    #    $data->{-afmfile}=_look_for_fontfile($data->{-afmfile});
    #    return(PDF::API2::Resource::Font::Postscript->new($pdf,$data->{-pfbfile},$data->{-afmfile},@opts));
    #}
    #elsif(defined $data->{-gfx}) 
    #{ # to be written and tested in 'Maki' first!
    #    return(PDF::API2::Resource::Font::gFont->new($pdf,$data,@opts);
    #}
    
    $class = ref $class if ref $class;
    $self = $class->SUPER::new($pdf, $data->{apiname}.pdfkey().'~'.time());
    $pdf->new_obj($self) unless($self->is_obj($pdf));
    $self->{' data'}=$data;
    $self->{-dokern}=1 if($opts{-dokern});

    $self->{'Subtype'} = PDFName($self->data->{type});
    $self->{'BaseFont'} = PDFName($self->fontname);
    if($opts{-pdfname}) 
    {
        $self->name($opts{-pdfname});
    }

    unless($self->data->{iscore}) 
    {
        $self->{'FontDescriptor'}=$self->descrByData();
    }

    $self->encodeByData($opts{-encode});

    return($self);
}

=item $font = PDF::API2::Resource::Font::CoreFont->new_api $api, $fontname, %options

Returns a corefont object. This method is different from 'new' that
it needs an PDF::API2-object rather than a PDF::API2::PDF::File-object.

=cut

sub new_api 
{
    my ($class,$api,@opts)=@_;

    my $obj=$class->new($api->{pdf},@opts);

    $api->{pdf}->new_obj($obj) unless($obj->is_obj($api->{pdf}));

##  $api->resource('Font',$obj->name,$obj);

    $api->{pdf}->out_obj($api->{pages});
    return($obj);
}

=item PDF::API2::Resource::Font::CoreFont->loadallfonts()

"Requires in" all fonts available as corefonts.

=cut

sub loadallfonts 
{
    foreach my $f (qw[ 
        courier courierbold courierboldoblique courieroblique
        georgia georgiabold georgiabolditalic georgiaitalic
        helveticaboldoblique helveticaoblique helveticabold helvetica
        symbol
        timesbolditalic timesitalic timesroman timesbold
        univers universbold
        verdana verdanabold verdanabolditalic verdanaitalic
        webdings
        wingdings
        zapfdingbats
    ])
    {
        _look_for_font($f);
    }
}

#    andalemono
#    arialrounded
#    bankgothic
#    impact
#    ozhandicraft
#    trebuchet
#    trebuchetbold
#    trebuchetbolditalic
#    trebuchetitalic

BEGIN 
{

    $alias = {
        ## Windows Fonts with Type1 equivalence
        'arial'                     => 'helvetica',
        'arialitalic'               => 'helveticaoblique',
        'arialbold'                 => 'helveticabold',
        'arialbolditalic'           => 'helveticaboldoblique',

        'times'                     => 'timesroman',
        'timesnewromanbolditalic'   => 'timesbolditalic',
        'timesnewromanbold'         => 'timesbold',
        'timesnewromanitalic'       => 'timesitalic',
        'timesnewroman'             => 'timesroman',

        'couriernewbolditalic'      => 'courierboldoblique',
        'couriernewbold'            => 'courierbold',
        'couriernewitalic'          => 'courieroblique',
        'couriernew'                => 'courier',
    };

    $subs = {
        #'bankgothicbold' => {
        #    'apiname'       => 'Bg2',
        #    '-alias'        => 'bankgothic',
        #    'fontname'      => 'BankGothicMediumBT,Bold',
        #    'flags'         => 32+262144,
        #},
        #'bankgothicbolditalic' => {
        #    'apiname'       => 'Bg3',
        #    '-alias'        => 'bankgothic',
        #    'fontname'      => 'BankGothicMediumBT,BoldItalic',
        #    'italicangle'   => -15,
        #    'flags'         => 96+262144,
        #},
        #'bankgothicitalic' => {
        #    'apiname'       => 'Bg4',
        #    '-alias'        => 'bankgothic',
        #    'fontname'      => 'BankGothicMediumBT,Italic',
        #    'italicangle'   => -15,
        #    'flags'         => 96,
        #},
        #  'impactitalic'      => {
        #            'apiname' => 'Imp2',
        #            '-alias'  => 'impact',
        #            'fontname'  => 'Impact,Italic',
        #            'italicangle' => -12,
        #          },
        #  'ozhandicraftbold'    => {
        #            'apiname' => 'Oz2',
        #            '-alias'  => 'ozhandicraft',
        #            'fontname'  => 'OzHandicraftBT,Bold',
        #            'italicangle' => 0,
        #            'flags' => 32+262144,
        #          },
        #  'ozhandicraftitalic'    => {
        #            'apiname' => 'Oz3',
        #            '-alias'  => 'ozhandicraft',
        #            'fontname'  => 'OzHandicraftBT,Italic',
        #            'italicangle' => -15,
        #            'flags' => 96,
        #          },
        #  'ozhandicraftbolditalic'  => {
        #            'apiname' => 'Oz4',
        #            '-alias'  => 'ozhandicraft',
        #            'fontname'  => 'OzHandicraftBT,BoldItalic',
        #            'italicangle' => -15,
        #            'flags' => 96+262144,
        #          },
        #  'arialroundeditalic'  => {
        #            'apiname' => 'ArRo2',
        #            '-alias'  => 'arialrounded',
        #            'fontname'  => 'ArialRoundedMTBold,Italic',
        #            'italicangle' => -15,
        #            'flags' => 96+262144,
        #          },
        #  'arialitalic'  => {
        #            'apiname' => 'Ar2',
        #            '-alias'  => 'arial',
        #            'fontname'  => 'Arial,Italic',
        #            'italicangle' => -15,
        #            'flags' => 96,
        #          },
        #  'arialbolditalic'  => {
        #            'apiname' => 'Ar3',
        #            '-alias'  => 'arial',
        #            'fontname'  => 'Arial,BoldItalic',
        #            'italicangle' => -15,
        #            'flags' => 96+262144,
        #          },
        #  'arialbold'  => {
        #            'apiname' => 'Ar4',
        #            '-alias'  => 'arial',
        #            'fontname'  => 'Arial,Bold',
        #            'flags' => 32+262144,
        #          },
    };

    $fonts = { };

}

1;

__END__

=back

=head1 SUPPORTED FONTS

=item PDF::API::CoreFont supports the following 'Adobe Core Fonts':

  Courier
  Courier-Bold
  Courier-BoldOblique
  Courier-Oblique
  Helvetica
  Helvetica-Bold
  Helvetica-BoldOblique
  Helvetica-Oblique
  Symbol
  Times-Bold
  Times-BoldItalic
  Times-Italic
  Times-Roman
  ZapfDingbats

=item PDF::API::CoreFont supports the following 'Windows Fonts':

  Georgia
  Georgia,Bold
  Georgia,BoldItalic
  Georgia,Italic
  Verdana
  Verdana,Bold
  Verdana,BoldItalic
  Verdana,Italic
  Webdings
  Wingdings

=head1 AUTHOR

alfred reibenschuh

=head1 HISTORY

    $Log: CoreFont.pm,v $
    Revision 2.0  2005/11/16 02:18:14  areibens
    revision workaround for SF cvs import not to screw up CPAN

    Revision 1.2  2005/11/16 01:27:50  areibens
    genesis2

    Revision 1.1  2005/11/16 01:19:27  areibens
    genesis

    Revision 1.17  2005/10/19 19:15:12  fredo
    added handling of optional kerning

    Revision 1.16  2005/10/01 22:41:07  fredo
    fixed font-naming race condition for multiple document updates

    Revision 1.15  2005/09/26 20:07:19  fredo
    added fontmetric stub

    Revision 1.14  2005/09/12 16:56:20  fredo
    applied mod_perl patch by Paul Schilling <pfschill@sbcglobal.net>

    Revision 1.13  2005/06/17 19:44:03  fredo
    fixed CPAN modulefile versioning (again)

    Revision 1.12  2005/06/17 18:53:34  fredo
    fixed CPAN modulefile versioning (dislikes cvs)

    Revision 1.11  2005/05/29 09:47:38  fredo
    cosmetic changes

    Revision 1.10  2005/03/14 22:01:27  fredo
    upd 2005

    Revision 1.9  2005/01/21 10:04:15  fredo
    rewrite fontproxy comment

    Revision 1.8  2004/12/16 00:30:54  fredo
    added no warn for recursion

    Revision 1.7  2004/11/22 02:08:42  fredo
    aaa

    Revision 1.6  2004/06/21 22:25:44  fredo
    added custom corefont handling

    Revision 1.5  2004/06/15 09:14:53  fredo
    removed cr+lf

    Revision 1.4  2004/06/07 19:44:43  fredo
    cleaned out cr+lf for lf

    Revision 1.3  2003/12/08 13:06:01  Administrator
    corrected to proper licencing statement

    Revision 1.2  2003/11/30 17:32:48  Administrator
    merged into default

    Revision 1.1.1.1.2.2  2003/11/30 16:57:05  Administrator
    merged into default

    Revision 1.1.1.1.2.1  2003/11/30 14:45:22  Administrator
    added CVS id/log


=cut


