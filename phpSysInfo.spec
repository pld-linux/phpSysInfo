Summary:	phpSysInfo is a PHP script that displays information about the host being accessed.
Summary(pl):	phpSysInfo jest skryptem PHP wyświetlającym informacje o wywołanym hoscie.
Name:		phpSysInfo
Version:	2.1
Release:	1
License:	GPL
# not sure about this Group:
Group:		Networking/Utilities
Vendor:		Uriah Welcome <precision@users.sourceforge.net>
Source0:	http://prdownloads.sourceforge.net/phpsysinfo/%{name}-%{version}.tar.gz
URL:		http://phpsysinfo.sourceforge.net
Requires:	php
Requires:	php-xml
Requires:	php-pcre
Requires:	webserver
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         _phpsysinfodir     /home/httpd/html/phpSysInfo

%description
PHPSysInfo is a customizable PHP Script that parses /proc, and formats
information nicely. It will display information about system facts
like Uptime, CPU, Memory, PCI devices, SCSI devices, IDE devices,
Network adapters, Disk usage, and more.

# TODO #%description -l pl

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_phpsysinfodir}/{includes/{lang,os,xml},templates/{aq,aq/images,black/images,blue,blue/images,classic,classic/images,metal,metal/images,orange,orange/images}}

install index.php phpsysinfo.dtd $RPM_BUILD_ROOT%{_phpsysinfodir}
install includes/*.php $RPM_BUILD_ROOT%{_phpsysinfodir}/includes
install includes/lang/*.php $RPM_BUILD_ROOT%{_phpsysinfodir}/includes/lang
install includes/os/*.php $RPM_BUILD_ROOT%{_phpsysinfodir}/includes/os
install includes/xml/*.php $RPM_BUILD_ROOT%{_phpsysinfodir}/includes/xml

install templates/aq/*.{css,tpl} $RPM_BUILD_ROOT%{_phpsysinfodir}/templates/aq
install templates/aq/images/*.gif $RPM_BUILD_ROOT%{_phpsysinfodir}/templates/aq/images
install templates/black/*.{css,tpl} $RPM_BUILD_ROOT%{_phpsysinfodir}/templates/black
install templates/black/images/*.gif $RPM_BUILD_ROOT%{_phpsysinfodir}/templates/black/images
install templates/blue/*.{css,tpl} $RPM_BUILD_ROOT%{_phpsysinfodir}/templates/blue
install templates/blue/images/*.gif $RPM_BUILD_ROOT%{_phpsysinfodir}/templates/blue/images
install templates/classic/*.{css,tpl} $RPM_BUILD_ROOT%{_phpsysinfodir}/templates/classic
install templates/classic/images/*.gif $RPM_BUILD_ROOT%{_phpsysinfodir}/templates/classic/images
install templates/metal/*.{css,tpl} $RPM_BUILD_ROOT%{_phpsysinfodir}/templates/metal
install templates/metal/images/*.gif $RPM_BUILD_ROOT%{_phpsysinfodir}/templates/metal/images
install templates/orange/*.{css,tpl} $RPM_BUILD_ROOT%{_phpsysinfodir}/templates/orange
install templates/orange/images/*.gif $RPM_BUILD_ROOT%{_phpsysinfodir}/templates/orange/images

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README ChangeLog
%dir %{_phpsysinfodir}
%{_phpsysinfodir}/index.php
%{_phpsysinfodir}/phpsysinfo.dtd
%{_phpsysinfodir}/includes
%{_phpsysinfodir}/templates
