%define		destdir		   /usr/local/afni/%{version}
%define         modulesdestination /usr/local/share/Modules/modulefiles/afni

Name:		afni%{version}
Version:	20141017
Release:	4%{?dist}
Summary:	Free software for analysis and display of FMRI data
License:	GPLv2+Other
URL:		http://afni.nimh.nih.gov/
Source0:	http://afni.nimh.nih.gov/pub/dist/tgz/afni_src.tgz
Patch1:		fixes.patch
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:	glib2-devel netpbm-devel openmotif-devel
BuildRequires:	expat-devel tcsh R-devel gcc-gfortran
BuildRequires:	libXpm-devel gsl-devel freeglut-devel libjpeg-devel compat-gcc-34
Requires:	glib2 netpbm openmotif expat tcsh libXpm gsl freeglut libjpeg
Requires:	environment-modules

%description
AFNI is a set of C programs for processing, analyzing, and displaying
functional MRI (FMRI) data - a technique for mapping human brain activity.
It runs on Unix+X11+Motif systems, including SGI, Solaris, Linux, and
Mac OS X. It is available free (in C source code format, and some
precompiled binaries) for research purposes.

%package devel
Summary: Development Libraries for afni
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Development Libraries and Headers for afni

%prep
%setup -q -n afni_src
%patch1 -p1 -b .fixes
%ifarch x86_64
cp Makefile.linux_openmp_64 Makefile
%else
cp Makefile.linux_openmp Makefile
%endif
# where we will install
perl -pi -e 's|INSTALLDIR = |INSTALLDIR = %{destdir}|' Makefile

%build
make clean
make all
make plugins

%install
rm -rf %{buildroot}
make install INSTALLDIR=%{buildroot}%{destdir}
make install_plugins INSTALLDIR=%{buildroot}%{destdir}
make install_lib INSTALLDIR=%{buildroot}%{destdir}
mkdir -p %{buildroot}%{modulesdestination}
cat > %{buildroot}%{modulesdestination}/%{version} <<ENDMODULE
#%Module1.0#####################################################################
##
## afni Module
##
proc ModulesHelp { } {
        global version

        puts stderr "\tThis module sets appropriate paths for using afni %{version}"
        puts stderr "\t"
        puts stderr "\n\tVersion \$version\n"
}

module-whatis   "Loads settings for afni %{version}"
prepend-path    PATH                    %{destdir}
prepend-path    LD_LIBRARY_PATH         %{destdir}
setenv		OMP_NUM_THREADS		1
set     version      "3.2.3"
ENDMODULE


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%dir /usr/local/afni
%{destdir}
%exclude %{destdir}/lib*a
%dir %{modulesdestination}
%{modulesdestination}/%{version}

%files devel
%defattr(-,root,root,-)
%{destdir}/lib*a

%changelog
* Wed Nov  4 2015 Adrian Alves <alvesadrian@fedoraproject.org> -1
- Initial Build for Fedora

* Tue May 21 2013 Josko Plazonic <plazonic@math.princeton.edu>
- initial build
