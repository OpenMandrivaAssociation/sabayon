%define pygtk2_version 2.5.3
%define gnome_python2_version 2.6.0

Name:    sabayon
Version: 2.20.1
Release: %mkrel 1
Summary: Tool to maintain user profiles in a GNOME desktop

Group:   System/Configuration/Other
License: GPL
URL:     http://www.gnome.org/projects/sabayon
Source0: http://ftp.gnome.org/pub/GNOME/sources/sabayon/sabayon-%{version}.tar.bz2
Patch: sabayon-2.12.3-pam.patch
# (fc) 2.12.1-3mdk source xinit file
Patch1:  sabayon-2.12.1-source.patch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

Requires: python-gamin
Requires: python-libxml2
Requires: python-ldap
Requires: GConf2 > 2.14.0-1mdk

BuildRequires: pygtk2.0-devel
BuildRequires: gtk+2-devel
BuildRequires: gettext
BuildRequires: desktop-file-utils
BuildRequires: usermode
BuildRequires: x11-server-xnest
BuildRequires: perl-XML-Parser

%description
Sabayon is a tool to help sysadmins and user change and maintain the
default behaviour of the GNOME desktop.

%package  admin
Summary:  Graphical tools for Sabayon profile management
Group:    System/Configuration/Other
Requires: %{name} = %{version}
Requires(pre):  rpm-helper
Requires(pre): usermode-consoleonly
Requires(post): gtk+2.0
Requires(postun): gtk+2.0
Requires: x11-server-xnest
Requires: pygtk2.0 >= %{pygtk2_version}
Requires: gnome-python-gconf >= %{gnome_python2_version}

%description admin
The sabayon-admin package contains the graphical tools which a
sysadmin should use to manage Sabayon profiles.

%prep
%setup -q
%patch -p1
%patch1 -p1 -b .source
#touch *
bzip2 -9 ChangeLog
 
%build
%configure2_5x 	\
	--enable-consolehelper=yes		\
	 --with-prototype-user=%{name}-admin
%make

%install
rm -rf $RPM_BUILD_ROOT

%makeinstall PAM_PREFIX=$RPM_BUILD_ROOT%{_sysconfdir}

desktop-file-install --vendor="" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications \
  --remove-category SystemSetup \
  --remove-category Application \
  --add-category "Settings;DesktopSettings" \
  --add-category X-MandrivaLinux-System-Configuration-GNOME \
  $RPM_BUILD_ROOT%{_datadir}/applications/%{name}.desktop

%find_lang sabayon


# We don't want these
rm -f %buildroot%py_platsitedir/%{name}/xlib.*a \
      %buildroot%_datadir/icons/hicolor/icon-theme.cache

%clean
rm -rf $RPM_BUILD_ROOT

%pre admin
%_pre_useradd %name-admin /var/lib/ /sbin/nologin
/usr/sbin/usermod -d "" %{name}-admin &>/dev/null || :

%post admin
%update_menus
%update_icon_cache hicolor

%postun admin
%clean_menus
%clean_icon_cache hicolor

%files -f sabayon.lang
%defattr(-, root, root, 755)

%doc AUTHORS ChangeLog.bz2 NEWS README TODO ISSUES

%config(noreplace) %{_sysconfdir}/X11/xinit.d/%{name}*

%{_sysconfdir}/desktop-profiles

%{_sbindir}/%{name}-apply

%dir %py_platsitedir/%{name}/
%py_platsitedir/%{name}/__init__.py*
%py_platsitedir/%{name}/config.py*
%py_platsitedir/%{name}/cache.py*
%py_platsitedir/%{name}/dirmonitor.py*
%py_platsitedir/%{name}/mozilla_bookmarks.py*
%py_platsitedir/%{name}/storage.py*
%py_platsitedir/%{name}/userdb.py*
%py_platsitedir/%{name}/userprofile.py*
%py_platsitedir/%{name}/util.py*
%py_platsitedir/%{name}/sources/*.py*

%files admin
%doc doc/index.html doc/testing.html doc/helping.html doc/developing.html
%doc doc/sabayon.css doc/*.jpg doc/*.gif

%config(noreplace) %{_sysconfdir}/pam.d/%{name}
%config(noreplace) %{_sysconfdir}/security/console.apps/%{name}

%{_bindir}/%{name}
%{_sbindir}/%{name}
%{_libexecdir}/%{name}*

%{_datadir}/%{name}/glade/%{name}.glade
%{_datadir}/%{name}/glade/pessulus.glade
%{_datadir}/applications/%{name}.desktop
%{_datadir}/icons/hicolor/*/apps/%{name}.*

%dir %py_platsitedir/%{name}
%py_platsitedir/%{name}/*.so
%py_platsitedir/%{name}/*


