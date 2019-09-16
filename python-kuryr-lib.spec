# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}
%global with_doc 1

%global project kuryr
%global library kuryr-lib
%global egg kuryr_lib

%global common_desc OpenStack Kuryr library shared by all Kuryr sub-projects.

Name: python-%library
Version: 1.1.1
Release: 1%{?dist}
Summary: OpenStack Kuryr library
License:    ASL 2.0
URL:        http://docs.openstack.org/developer/kuryr

Source0:    https://tarballs.openstack.org/%{project}/%{library}-%{upstream_version}.tar.gz

BuildArch: noarch

BuildRequires:  git
BuildRequires:  openstack-macros

%package -n python%{pyver}-%{library}
Summary: OpenStack Kuryr library
%{?python_provide:%python_provide python%{pyver}-%{library}}


BuildRequires:  python%{pyver}-ddt
BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-oslotest
BuildRequires:  python%{pyver}-pbr
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-testtools
# Required for tests
BuildRequires:  python%{pyver}-keystoneauth1
BuildRequires:  python%{pyver}-neutronclient
BuildRequires:  python%{pyver}-oslo-concurrency
BuildRequires:  python%{pyver}-oslo-config
BuildRequires:  python%{pyver}-oslo-log
BuildRequires:  python%{pyver}-oslo-utils
BuildRequires:  python%{pyver}-oslo-upgradecheck
BuildRequires:  python%{pyver}-pyroute2

Requires:       python%{pyver}-keystoneauth1 >= 3.4.0
Requires:       python%{pyver}-neutronclient >= 6.7.0
Requires:       python%{pyver}-neutron-lib >= 1.13.0
Requires:       python%{pyver}-oslo-concurrency >= 3.25.0
Requires:       python%{pyver}-oslo-config >= 2:5.2.0
Requires:       python%{pyver}-oslo-i18n >= 3.15.3
Requires:       python%{pyver}-oslo-log >= 3.36.0
Requires:       python%{pyver}-oslo-utils >= 3.33.0
Requires:       python%{pyver}-oslo-upgradecheck >= 0.1.0
Requires:       python%{pyver}-pbr >= 2.0.0
Requires:       python%{pyver}-babel >= 2.3.4
Requires:       python%{pyver}-pyroute2 >= 0.4.21
Requires:       python%{pyver}-six >= 1.10.0

# Handle python2 exception
%if %{pyver} == 2
Requires:       python-ipaddress >= 1.0.16
%endif

%description -n python%{pyver}-%{library}
%{common_desc}

%package -n python%{pyver}-%{library}-tests
Summary:    OpenStack Kuryr library tests
Requires:   python%{pyver}-%{library} = %{version}-%{release}
Requires:   python%{pyver}-ddt
Requires:   python%{pyver}-oslotest
Requires:   python%{pyver}-testtools

%description -n python%{pyver}-%{library}-tests
%{common_desc}

This package contains the Kuryr library test files.

%if 0%{?with_doc}
%package doc
Summary:    OpenStack Kuryr library documentation

BuildRequires: python%{pyver}-sphinx
BuildRequires: python%{pyver}-reno
BuildRequires: python%{pyver}-openstackdocstheme

%description doc
%{common_desc}

This package contains the documentation.
%endif

%package -n kuryr-binding-scripts
Summary:    OpenStack Kuryr binding scripts for SDNs

Requires: bash
Requires: iproute

%description -n kuryr-binding-scripts
%{common_desc}

This package contains the binding scripts for different SDNs.

%description
%{common_desc}

%prep
%autosetup -n %{library}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
%py_req_cleanup

%build
%{pyver_build}

%if 0%{?with_doc}
# generate html docs
export PYTHONPATH=.
sphinx-build-%{pyver} -b html doc/source doc/build/html
# remove the sphinx-build-%{pyver} leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{pyver_install}

%check
%{pyver_bin} setup.py test

%files -n python%{pyver}-%{library}
%license LICENSE
%{_bindir}/%{project}-status
%{pyver_sitelib}/%{project}
%{pyver_sitelib}/%{egg}-*.egg-info
%exclude %{pyver_sitelib}/%{project}/tests

%files -n python%{pyver}-%{library}-tests
%license LICENSE
%{pyver_sitelib}/%{project}/tests

%if 0%{?with_doc}
%files doc
%license LICENSE
%doc doc/build/html README.rst
%endif

%files -n kuryr-binding-scripts
%license LICENSE
%{_libexecdir}/kuryr

%changelog
* Mon Sep 16 2019 RDO <dev@lists.rdoproject.org> 1.1.1-1
- Update to 1.1.1

