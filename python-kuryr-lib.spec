%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global project kuryr
%global library kuryr-lib
%global egg kuryr_lib

%if 0%{?fedora} >= 24
%global with_python3 1
%endif

%global common_desc OpenStack Kuryr library shared by all Kuryr sub-projects.

Name: python-%library
Version: 0.8.0
Release: 1%{?dist}
Summary: OpenStack Kuryr library
License:    ASL 2.0
URL:        http://docs.openstack.org/developer/kuryr

Source0:    https://tarballs.openstack.org/%{project}/%{library}-%{upstream_version}.tar.gz

BuildArch: noarch

BuildRequires:  git
BuildRequires:  openstack-macros

%package -n python2-%{library}
Summary: OpenStack Kuryr library
%{?python_provide:%python_provide python2-%{library}}


BuildRequires:  python2-ddt
BuildRequires:  python2-devel
BuildRequires:  python2-oslotest
BuildRequires:  python2-pbr
BuildRequires:  python2-setuptools
BuildRequires:  python2-testtools
# Required for tests
BuildRequires:  python2-keystoneauth1
BuildRequires:  python2-neutronclient
BuildRequires:  python2-oslo-concurrency
BuildRequires:  python2-oslo-config
BuildRequires:  python2-oslo-log
BuildRequires:  python2-oslo-utils
BuildRequires:  python2-pyroute2

Requires:       python2-keystoneauth1 >= 3.4.0
Requires:       python2-neutronclient >= 6.7.0
Requires:       python2-neutron-lib >= 1.13.0
Requires:       python2-oslo-concurrency >= 3.25.0
Requires:       python2-oslo-config >= 2:5.2.0
Requires:       python2-oslo-i18n >= 3.15.3
Requires:       python2-oslo-log >= 3.36.0
Requires:       python2-oslo-utils >= 3.33.0
Requires:       python2-pbr >= 2.0.0
Requires:       python2-babel >= 2.3.4
Requires:       python2-pyroute2 >= 0.4.21
Requires:       python2-six >= 1.10.0
%if 0%{?fedora} || 0%{?rhel} > 7
Requires:       python2-ipaddress >= 1.0.16
%else
Requires:       python-ipaddress >= 1.0.16
%endif

%description -n python2-%{library}
%{common_desc}

%package -n python2-%{library}-tests
Summary:    OpenStack Kuryr library tests
Requires:   python2-%{library} = %{version}-%{release}
Requires:   python2-ddt
Requires:   python2-oslotest
Requires:   python2-testtools

%description -n python2-%{library}-tests
%{common_desc}

This package contains the Kuryr library test files.

%package doc
Summary:    OpenStack Kuryr library documentation

BuildRequires: python2-sphinx
BuildRequires: python2-reno
BuildRequires: python2-openstackdocstheme

%description doc
%{common_desc}

This package contains the documentation.

%package -n kuryr-binding-scripts
Summary:    OpenStack Kuryr binding scripts for SDNs

Requires: bash
Requires: iproute

%description -n kuryr-binding-scripts
%{common_desc}

This package contains the binding scripts for different SDNs.


%if 0%{?with_python3}
%package -n python3-%{library}
Summary: OpenStack Kuryr library
%{?python_provide:%python_provide python3-%{library}}

BuildRequires:  python3-ddt
BuildRequires:  python3-devel
BuildRequires:  python3-oslotest
BuildRequires:  python3-pbr
BuildRequires:  python3-setuptools
BuildRequires:  python3-testtools

# Required for tests
BuildRequires:  python3-keystoneauth1
BuildRequires:  python3-neutronclient
BuildRequires:  python3-oslo-concurrency
BuildRequires:  python3-oslo-config
BuildRequires:  python3-oslo-log
BuildRequires:  python3-oslo-utils
BuildRequires:  python3-pyroute2

Requires:       python3-keystoneauth1 >= 3.4.0
Requires:       python3-neutronclient >= 6.7.0
Requires:       python3-neutron-lib >= 1.13.0
Requires:       python3-oslo-concurrency >= 3.25.0
Requires:       python3-oslo-config >= 2:5.2.0
Requires:       python3-oslo-i18n >= 3.15.3
Requires:       python3-oslo-log >= 3.36.0
Requires:       python3-oslo-utils >= 3.33.0
Requires:       python3-pbr >= 2.0.0
Requires:       python3-babel >= 2.3.4
Requires:       python3-pyroute2 >= 0.4.21
Requires:       python3-six >= 1.10.0

%description -n python3-%{library}
%{common_desc}

This package contains the Python3 version of the library

%package -n python3-%{library}-tests
Summary:    OpenStack Kuryr library tests
Requires:   python3-%{library} = %{version}-%{release}
Requires:   python3-ddt
Requires:   python3-oslotest
Requires:   python3-testtools

%description -n python3-%{library}-tests
OpenStack Kuryr library containing the tests for all Kuryr sub-projects

This package contains the Python3 version of the library tests.

%endif # with_python3


%description
%{common_desc}

%prep
%autosetup -n %{library}-%{upstream_version} -S git

# Let's handle dependencies ourseleves
%py_req_cleanup

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif

# generate html docs
export PYTHONPATH=.
sphinx-build -b html doc/source doc/build/html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

%install
%py2_install
%if 0%{?with_python3}
%py3_install
%endif

%check
%{__python2} setup.py test
%if 0%{?with_python3}
rm -rf .testrepository
%{__python3} setup.py test
%endif

%files -n python2-%{library}
%license LICENSE
%{python2_sitelib}/%{project}
%{python2_sitelib}/%{egg}-*.egg-info
%exclude %{python2_sitelib}/%{project}/tests

%files -n python2-%{library}-tests
%license LICENSE
%{python2_sitelib}/%{project}/tests

%files doc
%license LICENSE
%doc doc/build/html README.rst

%files -n kuryr-binding-scripts
%license LICENSE
%{_libexecdir}/kuryr

%if 0%{?with_python3}
%files -n python3-%{library}
%license LICENSE
%{python3_sitelib}/%{project}
%{python3_sitelib}/%{egg}-*.egg-info
%exclude %{python3_sitelib}/%{project}/tests

%files -n python3-%{library}-tests
%license LICENSE
%{python3_sitelib}/%{project}/tests
%endif

%changelog
* Tue Aug 21 2018 RDO <dev@lists.rdoproject.org> 0.8.0-1
- Update to 0.8.0

