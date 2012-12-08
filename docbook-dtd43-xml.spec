%define name docbook-dtd43-xml
%define version 1.0
%define release %mkrel 13
%define dtdver 4.3
%define mltyp xml

Name: %{name}
Version: %{version}
Release: %{release}
Group       	: Publishing

Summary     	: XML document type definition for DocBook %{dtdver}

License   	: Artistic style
URL         	: http://www.oasis-open.org/docbook/

Provides        : docbook-dtd-%{mltyp}
Requires(post)	: coreutils
Requires(postun): coreutils
Requires(post)  : sgml-common >= 0.6.3-2mdk
Requires(postun): sgml-common >= 0.6.3-2mdk
Requires(post)  : libxml2-utils
Requires(postun): libxml2-utils

BuildRoot   	: %{_tmppath}/%{name}-%{version}-buildroot

# Zip file downloadable at http://www.oasis-open.org/docbook/%{mltyp}/%{dtdver}
Source0		: docbook-xml-%{dtdver}.tar.bz2 
BuildArch	: noarch  


%define sgmlbase %{_datadir}/sgml

%description
The DocBook Document Type Definition (DTD) describes the syntax of
technical documentation texts (articles, books and manual pages).
This syntax is XML-compliant and is developed by the OASIS consortium.
This is the version %{dtdver} of this DTD.


%prep
%setup -n docbook-xml-%{dtdver} -q

%build


%install
rm -rf %{buildroot}
DESTDIR=%{buildroot}%{sgmlbase}/docbook/%{mltyp}-dtd-%{dtdver}
mkdir -p $DESTDIR
cp -r ent/ $DESTDIR
install -m644 docbook.cat $DESTDIR/catalog
install -m644 catalog.xml $DESTDIR
install -m644 *.dtd $DESTDIR
install -m644 *.mod $DESTDIR
mkdir -p %{buildroot}%{_sysconfdir}/sgml
touch %{buildroot}%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat
# looks unnecesary
# touch %{buildroot}%{_sysconfdir}/sgml/catalog


%clean
rm -rf %{buildroot}


%files
%defattr (-,root,root)
%doc README ChangeLog
%{sgmlbase}/docbook/%{mltyp}-dtd-%{dtdver}
%ghost %config(noreplace) %{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat
# why this?
# %ghost %config(noreplace) %{_sysconfdir}/sgml/catalog


%post
##
## SGML catalog
##
%{_bindir}/xmlcatalog --sgml --noout --add \
	%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
	%{sgmlbase}/sgml-iso-entities-8879.1986/catalog
%{_bindir}/xmlcatalog --sgml --noout --add \
	%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
	%{sgmlbase}/docbook/%{mltyp}-dtd-%{dtdver}/catalog

# The following lines are for the case in which the style sheets
# were installed after another DTD but before this DTD
if [ -e %{sgmlbase}/openjade/catalog ]; then
	%{_bindir}/xmlcatalog --sgml --noout --add \
		%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
		%{sgmlbase}/openjade/catalog
fi

if [ -e %{sgmlbase}/docbook/dsssl-stylesheets/catalog ]; then
	%{_bindir}/xmlcatalog --sgml --noout --add \
		%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
		%{sgmlbase}/docbook/dsssl-stylesheets/catalog
fi
# Symlinks
[ ! -e %{_sysconfdir}/sgml/%{mltyp}-docbook.cat ] && \
	ln -s %{mltyp}-docbook-%{dtdver}.cat %{_sysconfdir}/sgml/%{mltyp}-docbook.cat

##
## XML catalog
##

CATALOG=%{sgmlbase}/docbook/xmlcatalog

%{_bindir}/xmlcatalog --noout --add "delegatePublic" \
	"-//OASIS//DTD DocBook XML V4.3//EN" \
	"file:///usr/share/sgml/docbook/xml-dtd-4.3/catalog.xml" $CATALOG
%{_bindir}/xmlcatalog --noout --add "rewriteSystem" \
	"http://www.oasis-open.org/docbook/xml/4.3" \
	"xml-dtd-4.3" $CATALOG
%{_bindir}/xmlcatalog --noout --add "rewriteURI" \
	"http://www.oasis-open.org/docbook/xml/4.3" \
	"xml-dtd-4.3" $CATALOG

%Postun
##
## SGML catalog
##
# Do not remove if upgrade
if [ "$1" = "0" ]; then
  if [ -x %{_bindir}/xmlcatalog ]; then 
	%{_bindir}/xmlcatalog --sgml --noout --del \
		%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
		%{sgmlbase}/sgml-iso-entities-8879.1986/catalog
	%{_bindir}/xmlcatalog --sgml --noout --del \
		%{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
		%{sgmlbase}/docbook/%{mltyp}-dtd-%{dtdver}/catalog
  fi
 # Symlinks
 [ -e %{_sysconfdir}/sgml/%{mltyp}-docbook.cat ] && \
	 rm -f %{_sysconfdir}/sgml/%{mltyp}-docbook.cat

 if [ -x %{_bindir}/xmlcatalog ]; then

  # The following lines are for the case in which the style sheets
  # were not uninstalled because there is still another DTD
  if [ -e %{sgmlbase}/openjade/catalog ]; then
	  %{_bindir}/xmlcatalog --sgml --noout --del \
		  %{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
		  %{sgmlbase}/openjade/catalog
  fi

  if [ -e %{sgmlbase}/docbook/dsssl-stylesheets/catalog ]; then
	  %{_bindir}/xmlcatalog --sgml --noout --del \
		  %{_sysconfdir}/sgml/%{mltyp}-docbook-%{dtdver}.cat \
		  %{sgmlbase}/docbook/dsssl-stylesheets/catalog
  fi
 fi

##
## XML catalog
##

  CATALOG=%{sgmlbase}/docbook/xmlcatalog

  if [ -w $CATALOG -a -x %{_bindir}/xmlcatalog ]; then
   %{_bindir}/xmlcatalog --noout --del \
  	   "-//OASIS//DTD DocBook XML V4.3//EN" $CATALOG
   %{_bindir}/xmlcatalog --noout --del \
	   "xml-dtd-4.3" $CATALOG
  fi
fi
 


%changelog
* Fri May 04 2012 Götz Waschk <waschk@mandriva.org> 1.0-13mdv2012.0
+ Revision: 795872
- fix file list for rpm5
- yearly rebuild

* Tue May 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0-12
+ Revision: 663834
- mass rebuild

* Thu Dec 02 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0-11mdv2011.0
+ Revision: 604804
- rebuild

* Tue Mar 16 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0-10mdv2010.1
+ Revision: 520689
- rebuilt for 2010.1

* Sun Aug 09 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0-9mdv2010.0
+ Revision: 413367
- rebuild

* Mon Jun 16 2008 Thierry Vignaud <tv@mandriva.org> 1.0-8mdv2009.0
+ Revision: 220673
- rebuild

* Sat Jan 12 2008 Thierry Vignaud <tv@mandriva.org> 1.0-7mdv2008.1
+ Revision: 149202
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Thu Aug 23 2007 Thierry Vignaud <tv@mandriva.org> 1.0-6mdv2008.0
+ Revision: 70195
- fileutils, sh-utils & textutils have been obsoleted by coreutils a long time ago

* Thu Aug 16 2007 Thierry Vignaud <tv@mandriva.org> 1.0-5mdv2008.0
+ Revision: 64214
- rebuild

* Sat Apr 28 2007 Adam Williamson <awilliamson@mandriva.org> 1.0-4mdv2008.0
+ Revision: 18837
- rebuild for new era


* Mon Jan 16 2006 Frederic Crozat <fcrozat@mandriva.com> 1.0-3mdk
- replace prereq

* Tue Nov 23 2004 Camille Begnis <camille@mandrakesoft.com> 1.0-2mdk
- fix license to please rpmlint
- added libxml2-utils prereq for xmlcatalog [Bug 12470]
- remove unneeded /etc/sgml/catalog

* Wed Nov 17 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 1.0-1mdk
- First package for Mdk

